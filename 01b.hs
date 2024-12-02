import Data.List (sort)
import System.IO (isEOF)

count :: Int -> [Int] -> Int
count el l = case l of
  [] -> 0
  h : t -> (if el == h then 1 else 0) + count el t

solve :: [Int] -> [Int] -> Int
solve l1 l2 = case l1 of
  [] -> 0
  h : t -> h * count h l2 + solve t l2

getInput :: IO ([Int], [Int])
getInput = do
  done <- isEOF
  if done
    then return ([], [])
    else do
      [h1, h2] <- map read . words <$> getLine :: IO [Int]
      (t1, t2) <- getInput
      return (h1 : t1, h2 : t2)

main :: IO ()
main = do
  (list1, list2) <- getInput
  print $ solve list1 list2
