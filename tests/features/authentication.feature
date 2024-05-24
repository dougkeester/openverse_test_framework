Feature: Authenticating to the Openverse API service
    As a consumer of the API,
    I want to register for authenticated use,
    So that I have greater access to the API.

    Scenario: API Returns Created Response
        Given I'm a new API user
        When I send a correctly formatted registration request
        Then I receive a 201 response

    #Scenario: API returns 400
    #    Given I'm a new API user
    #    When I send a registration request with my name missing
    #    Then I receive a 400 response


    #Scenario: API returns 401
    #    Given I'm a new API user


    #Scenario: API returns 429
    #    Given I'm a new API user

