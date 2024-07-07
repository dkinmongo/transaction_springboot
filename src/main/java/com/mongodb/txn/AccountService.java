package com.mongodb.txn;
import com.mongodb.ReadConcern;
import com.mongodb.ReadPreference;
import com.mongodb.TransactionOptions;
import com.mongodb.WriteConcern;
import com.mongodb.client.ClientSession;
import com.mongodb.client.MongoClient;
import com.mongodb.client.TransactionBody;
import com.mongodb.txn.model.Account;
import org.bson.Document;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.MongoTransactionManager;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Isolation;
import org.springframework.transaction.annotation.Transactional;

import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;

import java.util.Random;

@Service
public class AccountService {
    @Autowired
    MongoClient mongoClient;

    @Autowired
    private final MongoTemplate mongoTemplate;

    @Autowired
    private final MongoTransactionManager transactionManager;

    @Autowired
    public AccountService(MongoTemplate mongoTemplate, MongoTransactionManager transactionManager) {
        this.mongoTemplate = mongoTemplate;
        this.transactionManager = transactionManager;
    }

    @Transactional(isolation = Isolation.SERIALIZABLE)
    public void transferMoney() {
        Random random = new Random();

        // 출금 계좌 선택
        int from = random.nextInt(100);

        // 출금
        Query fromQuery = new Query(Criteria.where("_id").is(from));
        Update fromUpdate = new Update().inc("balance", -50);
        mongoTemplate.updateFirst(fromQuery, fromUpdate, Account.class);

        // 입금
        for (int i = 0; i < 50; i++) {
            int to = random.nextInt(100);
            Query toQuery = new Query(Criteria.where("_id").is(to));
            Update toUpdate = new Update().inc("balance", 1);
            mongoTemplate.updateFirst(toQuery, toUpdate, Account.class);
        }
    }
}
