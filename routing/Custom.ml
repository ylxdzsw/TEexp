open Core

open Apsp
open Util
open Yates_Types

open Yojson
open Yojson.Basic.Util

(***************)
(* local state *)
(***************)
let prev_scheme = ref SrcDstMap.empty

module VertMap = Map.Make(String)

let vname topo v = let Some x =
  let dotstr = Topology.Vertex.to_dot (Topology.vertex_to_label topo v) in
  let substrs = String.split dotstr ~on:' ' in
    (List.nth substrs 0) in
  x

(* call our algo *)
let call_python topo d : Yojson.Basic.json =
  let (cout, cin) = Unix.open_process "julia routing/yates_adapter.jl" in
    (* print topo *)
    let _ = Topology.fold_edges
    (fun e _ ->
      let src,_ = Topology.edge_src e in
      let dst,_ = Topology.edge_dst e in
      Printf.fprintf cin "%s %s\n" (vname topo src) (vname topo dst);
    0)
    topo 0 in
  
    Printf.fprintf cin "***\n";
  
    (* print demand *)
    SrcDstMap.fold ~init:0 ~f:(fun ~key:(src,dst) ~data:(demand) acc ->
      if demand > 0.0 then
        Printf.fprintf cin "%s %s\n" (vname topo src) (vname topo dst);
    0) d;
    
    Out_channel.close cin;
    Yojson.Basic.from_channel cout

(***********************)
(* algorithm interface *)
(***********************)

(* Initialization not needed *)
let initialize _ : unit = ()

(* Recovery: normalization recovery *)
let local_recovery = Util.normalization_recovery

let str_to_vert_pair dict pair_str =
  let (Some a, Some b) =
    let substrs = String.split pair_str ~on:' ' in
      ((List.nth substrs 0), (List.nth substrs 1)) in
  let (Some src, Some dst) =
    ((VertMap.find dict a), (VertMap.find dict b)) in
  (src, dst)

(* Solve: Uniform distributoin over k-shortest paths *)
let solve (topo:topology) (d:demands) budget : scheme =
  let new_scheme =
    if not (SrcDstMap.is_empty !prev_scheme) then !prev_scheme
    else
      let vert_dict = Topology.fold_vertexes
        (fun v acc -> VertMap.set acc ~key:(vname topo v) ~data:v)
        topo VertMap.empty in
    
      let json = call_python topo d in
      
      List.fold_left (json |> to_assoc) ~init:SrcDstMap.empty
      ~f:(fun acc (k, v) ->
        let path_map =
          let prob = 1.0 /. Float.of_int (List.length (v |> to_list)) in
          List.fold_left (v |> to_list) ~init:PathMap.empty
            ~f:(fun acc path ->
              let p = List.map (path |> to_list) (fun x ->
                let (src, dst) = str_to_vert_pair vert_dict (x |> to_string) in
                  Topology.find_edge topo src dst) in
              PathMap.set acc ~key:p ~data:prob
            ) in
        SrcDstMap.set acc ~key:(str_to_vert_pair vert_dict k) ~data:path_map
      ) in

  prev_scheme := new_scheme;
  new_scheme

let name = "Custom"