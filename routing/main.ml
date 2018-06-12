open Core

open Yates_Types
open Traffic
open Util

module type Algorithm = sig
    val solve : topology -> demands -> int -> scheme
    val name : string
end

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
        let x = if ecmp  then (module Ecmp  : Algorithm)::x else x in
        let x = if edksp then (module Edksp : Algorithm)::x else x in
        let x = if ksp   then (module Ksp   : Algorithm)::x else x in
        let x = if mcf   then (module Mcf   : Algorithm)::x else x in
        let x = if raeke then (module Raeke : Algorithm)::x else x in
        let x = if vlb   then (module Vlb   : Algorithm)::x else x in
        match x with
        | [] -> [(module Ecmp  : Algorithm);
                 (module Edksp : Algorithm);
                 (module Ksp   : Algorithm);
                 (module Mcf   : Algorithm);
                 (module Raeke : Algorithm);
                 (module Vlb   : Algorithm)]
        | _ -> x in

      let fname suffix = "data/" ^ data ^ suffix in
      let topo = Net.Parse.from_dotfile (fname ".dot") in
      let demands = all_demands (fname ".demands") (fname ".hosts") topo in
      
      List.iter algorithms (fun algo ->
        let module Algo = (val algo : Algorithm) in
        List.iteri demands (fun i demand ->
          let scheme = Algo.solve topo demand budget in
          let oc = Out_channel.create (data ^ "_" ^ Algo.name ^ "_" ^ (string_of_int i) ^ ".path") in
          fprintf oc "%s\n" (dump_scheme topo scheme);
          Out_channel.close oc
        )
      ))

let _ = Command.run command
