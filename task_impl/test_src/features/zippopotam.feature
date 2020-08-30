Feature: Test the RESTful APIs in the web site "api.zippopotam.us"

    Scenario: Execute the API test

        When we get zippopotam data from "http://api.zippopotam.us/de/bw/stuttgart"
        Then zippopotam's response status code is 200
         And zippopotam's response content type is "application/json"
         And zippopotam's response time is less than 1s
         And zippopotam's response data has fields as below
            | field     | value             |
            | country   | Germany           |
            | state     | Baden-Württemberg |
         And zippopotam's response data has place items as below
            | post code | place name            |
            | 70597     | Stuttgart Degerloch   |

    Scenario: Execute the API data-driven test

        When we run the data-driven test on zippopotam's data
            | country   | postal code   | place name    |
            | us        | 90210         | Beverly Hills |
            | us        | 12345         | Schenectady   |
            | ca        | B2R           | Waverley      |
