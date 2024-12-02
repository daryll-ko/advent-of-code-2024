import Data.List (sort)
import System.IO (isEOF)

listDistance :: [Int] -> [Int] -> Int
listDistance l1 l2 = case (l1, l2) of
  (h1 : t1, h2 : t2) -> abs (h1 - h2) + listDistance t1 t2
  ([], []) -> 0

solve :: [Int] -> [Int] -> Int
solve l1 l2 = listDistance (sort l1) (sort l2)

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
