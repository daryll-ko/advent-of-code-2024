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
      if grid[i][j] == 'A':
        var
          m = 0
          s = 0

        for d in 0..<4:
          let
            ii = i + @[-1, -1, 1, 1][d]
            jj = j + @[1, -1, -1, 1][d]

          if valid(ii, jj, r, c):
            case grid[ii][jj]
              of 'M':
                m += 1
              of 'S':
                s += 1
              else:
                discard

        if m == 2 and s == 2 and grid[i+1][j+1] != grid[i-1][j-1]:
          ans += 1

  return ans

proc main() =
  let
    grid = getGrid()
    ans = solve(grid)

  echo ans

main()
