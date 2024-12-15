proc getGrid(): seq[string] =
  var grid: seq[string] = @[]

  while true:
    try:
      var line = readLine(stdin)
      grid.add(line)
    except EOFError:
      break

  return grid

proc valid(i: int, j: int, r: int, c: int): bool =
  return 0 <= i and i < r and 0 <= j and j < c

proc solve(grid: seq[string]): int =
  let
    r = len(grid)
    c = len(grid[0])

  var ans = 0

  for i in 0..<r:
    for j in 0..<c:
      for d in 0..<8:
        var yay = true
        for s in 0..<4:
          let
            ii = i + s * @[0, -1, -1, -1, 0, 1, 1, 1][d]
            jj = j + s * @[1, 1, 0, -1, -1, -1, 0, 1][d]

          yay = yay and valid(ii, jj, r, c) and grid[ii][jj] == "XMAS"[s]

        if yay:
          ans += 1

  return ans

proc main() =
  let
    grid = getGrid()
    ans = solve(grid)

  echo ans

main()
