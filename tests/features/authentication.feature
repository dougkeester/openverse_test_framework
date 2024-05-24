Feature: Authenticating to the Openverse API service
    As a consumer of the API,
    I want to register for authenticated use,
    So that I have greater access to the API.

    # Disabling for now to avoid spamming registration. Remove the '@' tag to
    # enable the test.
    @do_not_run
    Scenario: API Returns Created Response
        Given I'm a new API user
        When I send a correctly formatted registration request
        Then I receive a 201 response

    Scenario: API Returns Bad Request Response When Name Missing
        Given I'm a new API user
        When I send a registration request with my name missing
        Then I receive a 400 response
    
    Scenario: API Returns Bad Request Response When Description Missing
        Given I'm a new API user
        When I send a registration request with the description missing
        Then I receive a 400 response

    Scenario: API Returns Bad Request Response When Email Missing
        Given I'm a new API user
        When I send a registration request with my email missing
        Then I receive a 400 response

    # Skipping this for now. I have not found a case where the registration API
    # will return a 401. Every negative case that I have tried returns 400.
    #Scenario: API returns 401
    #    Given I'm a new API user

    Scenario: API Returns Too Many Requests
        Given I'm a new API user
        When I send too many registration requests in a row
        Then I receive a 429 response

