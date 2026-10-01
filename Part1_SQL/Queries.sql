SELECT reseller_id , reseller_name , 
       SUM(order_amount) AS total_sales
FROM meesho
GROUP BY reseller_id , reseller_name
ORDER BY total_sales DESC;