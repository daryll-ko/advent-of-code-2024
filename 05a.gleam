import gleam/int
import gleam/io
import gleam/list
import gleam/option.{Some}
import gleam/regexp.{Match}
import gleam/result
import gleam/string
import gleam/yielder

pub fn extract(inp: String, delim delimiter: String) -> List(List(Int)) {
  inp
  |> string.split(on: "\n")
  |> yielder.from_list
  |> yielder.map(fn(line) {
    line
    |> string.split(on: delimiter)
    |> yielder.from_list
    |> yielder.map(fn(val) { val |> int.parse |> result.unwrap(or: 0) })
    |> yielder.to_list
  })
  |> yielder.to_list
}

pub fn cross(x: Int, l: List(Int)) -> List(#(Int, Int)) {
  case l {
    [] -> []
    [h, ..t] -> list.append([#(x, h)], cross(x, t))
  }
}

pub fn all_pairs(l: List(Int)) -> List(#(Int, Int)) {
  case l {
    [] -> []
    [h, ..t] -> list.append(cross(h, t), all_pairs(t))
  }
}

pub fn qualifies(update: List(Int), rules: List(List(Int))) -> Bool {
  update
  |> all_pairs
  |> yielder.from_list
  |> yielder.all(fn(pair) {
    let #(l1, r1) = pair
    rules
    |> yielder.from_list
    |> yielder.all(fn(rule) {
      case rule {
        [l2, r2] -> !{ l1 == r2 && r1 == l2 }
        _ -> False
      }
    })
  })
}

pub fn middle(update: List(Int)) -> Int {
  let update_yielder = update |> yielder.from_list
  let index =
    int.floor_divide(update_yielder |> yielder.length, 2)
    |> result.unwrap(or: 0)

  update_yielder
  |> yielder.at(index)
  |> result.unwrap(or: 0)
}

pub fn main() {
  let input = "Hi"

  let rules =
    "<redacted to not clutter the code>"
    |> extract(delim: "|")

  let updates =
    "<redacted to not clutter the code>"
    |> extract(delim: ",")

  let answer =
    updates
    |> yielder.from_list
    |> yielder.filter(fn(update) { qualifies(update, rules) })
    |> yielder.map(middle)
    |> yielder.reduce(fn(acc, x) { acc + x })
    |> result.unwrap(or: 0)
    |> io.debug
}
