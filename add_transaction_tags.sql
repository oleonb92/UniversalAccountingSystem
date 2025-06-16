-- Add tags to bar expenses
INSERT INTO transactions_transaction_tags (transaction_id, tag_id)
SELECT id, 4  -- fun tag
FROM transactions_transaction
WHERE description LIKE 'Gasto Bars%';

-- Add tags to coffee shop expenses
INSERT INTO transactions_transaction_tags (transaction_id, tag_id)
SELECT id, 3  -- food tag
FROM transactions_transaction
WHERE description LIKE 'Gasto Coffee Shops%';

-- Add monthly tag to all transactions
INSERT INTO transactions_transaction_tags (transaction_id, tag_id)
SELECT id, 2  -- monthly tag
FROM transactions_transaction
WHERE description LIKE 'Gasto%';

-- Add ai-analyzed tag to all transactions
INSERT INTO transactions_transaction_tags (transaction_id, tag_id)
SELECT id, 5  -- ai-analyzed tag
FROM transactions_transaction
WHERE description LIKE 'Gasto%'; 