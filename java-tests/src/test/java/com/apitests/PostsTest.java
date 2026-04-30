package com.apitests;

import io.restassured.RestAssured;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import java.util.HashMap;
import java.util.Map;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.equalTo;
import static org.hamcrest.Matchers.notNullValue;

/**
 * RestAssured tests for the JSONPlaceholder /posts endpoint.
 * Mirrors the Python pytest suite under tests/ to demonstrate that the
 * framework can run in a unified Java + Python stack.
 */
class PostsTest {

    @BeforeAll
    static void setBaseUri() {
        RestAssured.baseURI = "https://jsonplaceholder.typicode.com";
    }

    @Test
    @DisplayName("GET /posts/1 returns HTTP 200")
    void getSinglePostReturns200() {
        given()
            .when()
                .get("/posts/1")
            .then()
                .statusCode(200);
    }

    @Test
    @DisplayName("GET /posts/1 returns the expected fields")
    void getPostResponseContainsExpectedFields() {
        given()
            .when()
                .get("/posts/1")
            .then()
                .statusCode(200)
                .body("id", equalTo(1))
                .body("title", notNullValue())
                .body("body", notNullValue())
                .body("userId", notNullValue());
    }

    @ParameterizedTest(name = "GET /posts/{0} returns 200")
    @ValueSource(ints = {1, 2, 3, 4, 5})
    void getPostByIdReturns200(int postId) {
        given()
            .when()
                .get("/posts/" + postId)
            .then()
                .statusCode(200)
                .body("id", equalTo(postId));
    }

    @Test
    @DisplayName("GET /posts/9999 returns 404 (negative test)")
    void getNonexistentPostReturns404() {
        given()
            .when()
                .get("/posts/9999")
            .then()
                .statusCode(404);
    }

    @Test
    @DisplayName("POST /posts creates a resource and echoes the data")
    void createPostReturns201AndEchoesData() {
        Map<String, Object> newPost = new HashMap<>();
        newPost.put("title", "My first API test");
        newPost.put("body", "I am learning automation");
        newPost.put("userId", 1);

        given()
                .header("Content-Type", "application/json")
                .body(newPost)
            .when()
                .post("/posts")
            .then()
                .statusCode(201)
                .body("title", equalTo("My first API test"))
                .body("body", equalTo("I am learning automation"))
                .body("userId", equalTo(1))
                .body("id", notNullValue());
    }
}
