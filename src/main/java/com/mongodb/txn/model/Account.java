package com.mongodb.txn.model;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "accounts")
@Setter
@Getter
@NoArgsConstructor
public class Account {
    @Id
    private String id;
    private int balance;
}
