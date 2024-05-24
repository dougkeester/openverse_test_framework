@auth
Feature: Authenticating to the Openverse API service
    As a consumer of the API,
    I want to register for authenticated use,
    So that I have greater access to the API.

    # Disabling for now to avoid spamming registration. Remove the '@' tag to
    # enable the test.
    @do_not_run
    Scenario: API Returns Created Response
        Given I am a new API user
        When I send a correctly formatted registration request
        Then I receive a 201 response

    Scenario: API Returns Bad Request Response When Name Missing
        Given I am a new API user
        When I send a registration request with my name missing
        Then I receive a 400 response
    
    Scenario: API Returns Bad Request Response When Description Missing
        Given I am a new API user
        When I send a registration request with the description missing
        Then I receive a 400 response

    Scenario: API Returns Bad Request Response When Email Missing
        Given I am a new API user
        When I send a registration request with my email missing
        Then I receive a 400 response

    # Disabling for now to avoid false fails due to rate limiting
    @do_not_run
    Scenario: API Returns Too Many Requests
        Given I am a new API user
        When I send too many registration requests in a row
        Then I receive a 429 response
    
    Scenario: API Returns a Bearer Token To Registered User
        Given I am a registered API user
        When I request an auth token
        Then I receive a valid auth token

    Scenario: API Returns Bad Request When Token Data Missing
        Given I am a registered API user
        When I request an auth token with data missing
        Then I do not receive a token and get an error response
    
    Scenario: API Returns Unauthorized When Token Data Incomplete
        Given I am a registered API user
        When I request an auth token with incomplete data
        Then I do not receive a token and get an unauthorized response
