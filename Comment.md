**Show User**
----
  Returns json data about a single user.

* **URL**

  posts/:post_pk/comment

* **HEADER:**
  
  Authorization:<type=jwt> <credentials>
  ex)Authorization:jwt eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b......



* **Method:**

  GET, POST
  
*  **URL Params**

   **Required:**
 
   `post_pk=[integer]`

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** "{\"payload\": [{\"id\": 3, \"contents\": \"댓글\", \"created\": \"2020-02-07T13:51:18.936566+09:00\", \"modify_date\": \"2020-02-07T15:27:32.443929+09:00\", \"is_active\": true, \"delete_date\": null, \"user\": 9, \"post\": 1637}, \"message\": \"success create\"}"
 
* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ error : "User doesn't exist" }`

  OR

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ error : "You are unauthorized to make this request." }`

* **Sample Call:**

  ```java
    $.ajax({
      url: "/users/1",
      dataType: "json",
      type : "GET",
      success : function(r) {
        console.log(r);
      }
    });
  ```
