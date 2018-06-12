open Core

open Yates_Types

let open_demands (demand_file:string) (host_file:string) (topo:topology) : (index_map * In_channel.t) =
  let name_map =
    VertexSet.fold (Topology.vertexes topo)
    ~init:StringMap.empty
       ~f:(fun acc v ->
         let n = (Topology.vertex_to_label topo v) in
         (StringMap.set acc ~key:(Node.name n) ~data:v )) in
  let (_,host_map) =
    In_channel.with_file
      host_file
      ~f:(fun file ->
        In_channel.fold_lines file ~init:(0,IntMap.empty)
          ~f:(fun (i,m) line ->
            match (StringMap.find name_map line) with
            | None ->
              (* Ignore a host in host file if it is not in the topology subgraph  *)
              (i+1, m)
            | Some n ->
              (i+1, (IntMap.set m ~key:i ~data:n)))) in
  (host_map, (In_channel.create demand_file))

let close_demands (ic:In_channel.t) : unit =
  In_channel.close ic

let next_demand ?scale:(scale=1.0) (ic:In_channel.t) (host_map:index_map) : demands =
  let line =
    try
      In_channel.input_line_exn ic
    with e ->
      (* Wrap around when EOF is reached *)
      Printf.printf "Wrapping around...\n";
      In_channel.seek ic 0L;
      In_channel.input_line_exn ic
      (*close_in_noerr ic;
      raise e*)
  in
  let entries = Array.of_list (String.split line ~on:' ') in
  let size = Int.of_float (sqrt (Float.of_int (Array.length entries))) in
  let demands = ref SrcDstMap.empty in
  for i = 0 to (size-1) do
    for j = 0 to (size-1) do
      let s = IntMap.find host_map i in
      let d = IntMap.find host_map j in
      match (s,d) with
      | (Some s, Some d) ->
        (* Can't demand from yourself *)
        let v = if i = j then 0.0 else (scale *. Float.of_string (entries.((i*size) + j))) in
        demands := SrcDstMap.set !demands ~key:(s,d) ~data:v
      | _ -> () (* if i or j-th node in input demand matrix is not in subgraph,
                   ignore the corresponding (i,j) demand entry *)
    done
  done;
  !demands

let all_demands ?scale:(scale=1.0) (demand_file:string) (host_file:string) (topo:topology) : demands list =
  let (hm, ic) = open_demands demand_file host_file topo in

  let parse_line line =
    let entries = Array.of_list (String.split line ~on:' ') in
    let size = Int.of_float (sqrt (Float.of_int (Array.length entries))) in
    let demands = ref SrcDstMap.empty in
      for i = 0 to (size-1) do
        for j = 0 to (size-1) do
          let s = IntMap.find hm i in
          let d = IntMap.find hm j in
          match (s,d) with
          | (Some s, Some d) ->
            let v = if i = j then 0.0 else (scale *. Float.of_string (entries.((i*size) + j))) in
            demands := SrcDstMap.set !demands ~key:(s,d) ~data:v
          | _ -> ()
        done
      done; !demands in
      
  let rec f acc = 
    let line = try Some (In_channel.input_line_exn ic) with e -> None in
    match line with
    | Some line -> f (parse_line line::acc)
    | None -> acc in
    
  let demands = f [] in
  close_demands ic;
  demands
