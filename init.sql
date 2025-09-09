-- Initialize the AlgoEngine database with sample data

USE aae;

-- Insert sample problems
INSERT INTO problems (title, description, concept, stars, series_id, series_index, is_daily_candidate) VALUES
('Two Sum', 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.\n\nExample:\nInput: nums = [2,7,11,15], target = 9\nOutput: [0,1]\nExplanation: Because nums[0] + nums[1] == 9, we return [0, 1].', 'arrays', 1, 1, 1, true),

('Best Time to Buy and Sell Stock', 'You are given an array prices where prices[i] is the price of a given stock on the ith day.\n\nYou want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.\n\nReturn the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.\n\nExample:\nInput: prices = [7,1,5,3,6,4]\nOutput: 5\nExplanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.', 'arrays', 2, 1, 2, true),

('Contains Duplicate', 'Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.\n\nExample:\nInput: nums = [1,2,3,1]\nOutput: true\n\nExample 2:\nInput: nums = [1,2,3,4]\nOutput: false', 'arrays', 1, 1, 3, true),

('Valid Parentheses', 'Given a string s containing just the characters "(", ")", "{", "}", "[" and "]", determine if the input string is valid.\n\nAn input string is valid if:\n1. Open brackets must be closed by the same type of brackets.\n2. Open brackets must be closed in the correct order.\n\nExample:\nInput: s = "()"\nOutput: true\n\nExample 2:\nInput: s = "([)]"\nOutput: false', 'stack', 2, 2, 1, true),

('Binary Search', 'Given an array of integers nums which is sorted in ascending order, and an integer target, write a function to search target in nums. If target exists, then return its index. Otherwise, return -1.\n\nYou must write an algorithm with O(log n) runtime complexity.\n\nExample:\nInput: nums = [-1,0,3,5,9,12], target = 9\nOutput: 4\nExplanation: 9 exists in nums and its index is 4', 'binary search', 2, 3, 1, true),

('Sliding Window Maximum', 'You are given an array of integers nums, there is a sliding window of size k which is moving from the very left of the array to the very right. You can only see the k numbers in the window. Each time the sliding window moves right by one position.\n\nReturn the max sliding window.\n\nExample:\nInput: nums = [1,3,-1,-3,5,3,6,7], k = 3\nOutput: [3,3,5,5,6,7]', 'sliding window', 4, 4, 1, true);

-- Insert sample test cases for Two Sum
INSERT INTO testcases (problem_id, input_data, expected_output, is_sample) VALUES
(1, '[2,7,11,15]\n9', '[0,1]', true),
(1, '[3,2,4]\n6', '[1,2]', false),
(1, '[3,3]\n6', '[0,1]', false);

-- Insert sample test cases for Best Time to Buy and Sell Stock
INSERT INTO testcases (problem_id, input_data, expected_output, is_sample) VALUES
(2, '[7,1,5,3,6,4]', '5', true),
(2, '[7,6,4,3,1]', '0', true),
(2, '[1,2,3,4,5]', '4', false);

-- Insert sample test cases for Contains Duplicate
INSERT INTO testcases (problem_id, input_data, expected_output, is_sample) VALUES
(3, '[1,2,3,1]', 'true', true),
(3, '[1,2,3,4]', 'false', true),
(3, '[1,1,1,3,3,4,3,2,4,2]', 'true', false);

-- Insert sample test cases for Valid Parentheses
INSERT INTO testcases (problem_id, input_data, expected_output, is_sample) VALUES
(4, '()', 'true', true),
(4, '()[]{}', 'true', true),
(4, '([)]', 'false', true),
(4, '{[]}', 'true', false);

-- Insert sample test cases for Binary Search
INSERT INTO testcases (problem_id, input_data, expected_output, is_sample) VALUES
(5, '[-1,0,3,5,9,12]\n9', '4', true),
(5, '[-1,0,3,5,9,12]\n2', '-1', true),
(5, '[5]\n5', '0', false);

-- Insert sample test cases for Sliding Window Maximum
INSERT INTO testcases (problem_id, input_data, expected_output, is_sample) VALUES
(6, '[1,3,-1,-3,5,3,6,7]\n3', '[3,3,5,5,6,7]', true),
(6, '[1]\n1', '[1]', true),
(6, '[1,-1]\n1', '[1,-1]', false);