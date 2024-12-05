import gleam/int
import gleam/io
import gleam/option.{Some}
import gleam/regexp.{Match}
import gleam/result
import gleam/string
import gleam/yielder

pub fn solve(string, regex) {
  regexp.scan(with: regex, content: string)
  |> yielder.from_list
  |> yielder.map(fn(x) {
    case x {
      Match(_, submatches) ->
        case submatches {
          [Some(x), Some(y)] -> {
            result.unwrap(int.parse(x), 0) * result.unwrap(int.parse(y), 0)
          }
          _ -> 0
        }
    }
  })
  |> yielder.reduce(fn(acc, x) { acc + x })
  |> result.unwrap(or: 0)
}

pub fn main() {
  let assert Ok(re) = regexp.from_string("mul\\(([0-9]{1,3}),([0-9]{1,3})\\)")

  let input =
    "<redacted to not clutter the code>"

  let parts = input |> string.split(on: "don't()")

  case parts {
    [head, ..tail] ->
      solve(head, re)
      + {
        tail
        |> yielder.from_list
        |> yielder.map(fn(str) {
          let subparts =
            str
            |> string.split_once(on: "do()")
            |> result.unwrap(or: #("", ""))
          solve(subparts.1, re)
        })
        |> yielder.reduce(fn(acc, x) { acc + x })
        |> result.unwrap(or: 0)
      }
    _ -> 0
  }
  |> io.debug
}
