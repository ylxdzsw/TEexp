open Core

open Types

let command =
  Command.basic_spec
    ~summary:"find paths for demand pairs"
    Command.Spec.(
    empty
    +> flag "-ecmp" no_arg ~doc:" run ecmp"
    +> flag "-edksp" no_arg ~doc:" run edge-disjoint ksp"
    +> flag "-ksp" no_arg ~doc:" run ksp"
    +> flag "-mcf" no_arg ~doc:" run mcf"
    +> flag "-raeke" no_arg ~doc:" run raeke"
    +> flag "-vlb" no_arg ~doc:" run vlb"
    (* run all algorithms if no one is specified *)
    +> flag "-budget" (optional_with_default 32 int) ~doc:" max paths between each pair of hosts"
    +> anon ("data" %: string)
  ) (fun
    (ecmp:bool)
    (edksp:bool)
    (ksp:bool)
    (mcf:bool)
    (raeke:bool)
    (vlb:bool)
    (budget:int)
    (data:string)
    () ->
      let algorithms =
        let x = [] in
        let x = if ecmp  then Ecmp::x  else x in
        let x = if edksp then Edksp::x else x in
        let x = if ksp   then Ksp::x   else x in
        let x = if mcf   then Mcf::x   else x in
        let x = if raeke then Raeke::x else x in
        let x = if vlb   then Vlb::x   else x in
        match x with
        | [] -> [Ecmp; Edksp; Ksp; Mcf; Raeke; Vlb]
        | _ -> x in

      let fname suffix = "data/" ^ data ^ suffix in
      let topo = Net.Parse.from_dotfile (fname ".dot") in
      let demands = all_demands (fname ".demands") (fname ".hosts") topo in
      
      List.iter (fun algo ->
        List.iteri (fun i demand ->
          let scheme = algo.solve topo demand budget in
          let oc = Out_channel.create data ^ "_" ^ algo.name ^ "_" ^ (string_of_int i) ^ ".path" in
          fprintf oc "%s\n" (dump_scheme topo scheme);
          Out_channel.close oc
        )
      ) algorithms)

let _ = Command.run command
