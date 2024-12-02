import Data.List (reverse, sort)
import System.IO (isEOF)

gentle :: [Int] -> Bool
gentle l = case l of
  h1 : h2 : t -> 1 <= abs (h1 - h2) && abs (h1 - h2) <= 3 && gentle (h2 : t)
  _ -> True

increasing :: [Int] -> Bool
increasing l = case l of
  h1 : h2 : t -> h1 < h2 && increasing (h2 : t)
  _ -> True

ok :: [Int] -> Bool
ok l = (increasing l || (increasing . reverse) l) && gentle l

solve :: [[Int]] -> Int
solve ls = case ls of
  [] -> 0
  h : t -> (if ok h then 1 else 0) + solve t

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
