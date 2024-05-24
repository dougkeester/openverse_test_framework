@audio
Feature: Using the Openverse API audio endpoints
    As a consumer of the API,
    I want to use the audio API,
    So that I can find interesting audio to listen to.

    Scenario: Use the API to search for audio files
        Given I am a registered API user
        When I search using the audio API correctly
        Then I receive good search results data

    Scenario: Use the API to retrieve stats about content providers
        Given I am a registered API user
        When I call the stats endpoint correctly
        Then I receive good stats results data