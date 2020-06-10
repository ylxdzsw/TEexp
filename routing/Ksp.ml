open Core

open Apsp
open Util
open Yates_Types

let name = "Ksp"

let solve (topo:topology) (_:demands) budget: scheme =
  let raw_scheme =
      let host_set = get_hosts_set topo in
      let all_ksp = all_pair_k_shortest_path topo budget host_set in
      SrcDstMap.fold all_ksp ~init:SrcDstMap.empty
        ~f:(fun ~key:(u, v) ~data:paths acc ->
            if u = v then acc
            else
              let path_map =
                List.fold_left paths ~init:PathMap.empty
                  ~f:(fun acc path ->
                      (* let prob = 1.0 /. Float.of_int (List.length paths) in *)
                      let prob = 1.0 /. Float.of_int (List.length path) in
                      PathMap.set acc ~key:path ~data:prob) in
              SrcDstMap.set acc ~key:(u, v) ~data:path_map) in
  let normalized_scheme = normalize_scheme raw_scheme in
  normalized_scheme
