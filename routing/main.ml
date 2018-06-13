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
    Command.Spec.(empty
      +> flag "-budget" (optional_with_default 32 int) ~doc:" max paths between each pair of hosts"
      +> anon ("data" %: string)
    ) (fun (budget:int) (data:string) () ->
      let algorithms = [(module Ecmp  : Algorithm);
                        (module Edksp : Algorithm);
                        (module Ksp   : Algorithm);
                        (module Mcf   : Algorithm);
                        (module Raeke : Algorithm);
                        (module Vlb   : Algorithm)] in

      let fname suffix = "data/" ^ data ^ suffix in
      let topo = Net.Parse.from_dotfile (fname ".dot") in
      let demands = all_demands (fname ".demands") (fname ".hosts") topo in
      
      List.iter algorithms (fun algo ->
        let module Algo = (val algo : Algorithm) in
        List.iteri demands (fun i demand ->
          let scheme = Algo.solve topo demand budget in
          printf "***%s***\n\n%s\n" Algo.name (dump_scheme topo scheme)
        )
      ))

let _ = Command.run command
