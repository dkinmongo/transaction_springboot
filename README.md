# MongoDB Transaction Demo

This repository contains a demo to illustrate how MongoDB transactions work using a simple banking example. The demo simulates money transfers between accounts and monitors the consistency of account balances over time.

## Prerequisites

- MongoDB installed and running
- Python 3.x installed
- Spring Boot and Java Development Kit (JDK) installed

## Initial Data Loading

The initial data loading script populates the MongoDB database with 100 accounts, each starting with a balance of 100 units.

```javascript
db.accounts.drop()

for(a=0;a<100;a++) {
    db.accounts.insertOne({_id:a,balance:100})
}
```

## Transaction Logic in Spring Boot
This section describes the transaction logic used for withdrawing and depositing funds between accounts. The withdrawal amount is fixed at 50 units, and the deposit amount is distributed randomly to 50 different accounts.

```javascript
// Withdrawal Operation
Query fromQuery = new Query(Criteria.where("_id").is(from));
Update fromUpdate = new Update().inc("balance", -50);
mongoTemplate.updateFirst(fromQuery, fromUpdate, Account.class);

// Deposit Operation
for (int i = 0; i < 50; i++) {
    int to = random.nextInt(100);
    Query toQuery = new Query(Criteria.where("_id").is(to));
    Update toUpdate = new Update().inc("balance", 1);
    mongoTemplate.updateFirst(toQuery, toUpdate, Account.class);
}
```

## Monitoring
The monitoring script ensures that the total balance across all accounts remains constant, verifying the consistency of the transactions. It aggregates the total balance and prints it to the console every second.

```javascript
for (i=0; i< 1000000; i++){
  console.log(db.accounts.aggregate({$group:{_id:true,total:{$sum:"$balance"}}}))
  sleep(1000)
}
```

## Traffic Generator
To simulate load and test the performance of the transaction handling, use the provided Python script traffic_generator.py.

Run the script using the following command:

```
python3 traffic_generator.py
```

## Summary
This demo showcases the implementation of MongoDB transactions in a banking scenario using Spring Boot. It highlights the importance of maintaining data consistency and provides tools to monitor and simulate load on the system.

For more details and advanced configurations, please refer to the code in the repository.


