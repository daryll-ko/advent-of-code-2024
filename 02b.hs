import Data.List (reverse, sort)
import System.IO (isEOF)

-- list, comparison function, already violated
ok :: [Int] -> (Int -> Int -> Bool) -> Bool -> Bool
ok l cmp ohno = case l of
  h1 : h2 : h3 : t ->
    if cmp h2 h3 && 1 <= abs (h2 - h3) && abs (h2 - h3) <= 3
      then
        if cmp h1 h2 && 1 <= abs (h1 - h2) && abs (h1 - h2) <= 3
          then
            ok (h2 : h3 : t) cmp ohno
          else not ohno && (ok (h2 : h3 : t) cmp True || ok (h1 : h3 : t) cmp True)
      else not ohno && (ok (h1 : h3 : t) cmp True || ok (h1 : h2 : t) cmp True)
  [h1, h2] ->
    (cmp h1 h2 && 1 <= abs (h1 - h2) && abs (h1 - h2) <= 3) || not ohno
  _ -> True

solve :: [[Int]] -> Int
solve ls = case ls of
  [] -> 0
  h : t -> (if ok h (<) False || ok h (>) False then 1 else 0) + solve t

getInput :: IO [[Int]]
getInput = do
  done <- isEOF
  if done
    then return []
    else do
      h <- map read . words <$> getLine :: IO [Int]
      t <- getInput
      return (h : t)

main :: IO ()
main = do
  reports <- getInput
  print $ solve reports
