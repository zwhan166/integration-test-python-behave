
@fixture.browser.firefox
Feature: Partial test on Sogeti's website

    Scenario: Test the menu link "Automation" under menu "Services"

        When we load the web page "http://www.sogeti.com"
        Then the web page's title is "Sogeti, provider of technology and engineering services"

        When we hover menu "Services"
         And we click menu link "Services::Automation"
        Then the web page's title is "Automation"
         And the web page's heading is "Automation"

        When we hover menu "Services"
        Then menu "Services" is displayed as selected
         And menu link "Services::Automation" is displayed as selected

    Scenario: Test the contact form in the "Automation" page

        When we load the web page "http://www.sogeti.com"
         And we click menu "Services"
         And we click menu link "Services::Automation"
         And we scroll down to form "Contact us:"
         And we fill the contact form's text fields as below
            | field         | text                  |
            | First Name*   | foo              |
            | Last Name*    | bar                   |
            | Email*        | bar.foo@example.com    |
            | Phone         | +49 (0) 123 456 7890  |
            | Message*      | #automatically-generated-message# Please feel free to delete this. |
         And we click the contact form's check box "I agree"
         And we click the contact form's submit button
        Then the contact form displays success with message "Thank you for contacting us."

    Scenario: Test the web pages for other countries

        When we load the web page "http://www.sogeti.com"
        Then the country drop-down list is invisible

        When we click the drop-down button "Worldwide"
        Then the country drop-down list is visible
         And the country links are linked correctly
            | country       | result page title                 |
            | Belgium       | Sogeti Belgium                    |
            | Finland       | Sogeti Finland                    |
            | France        | Sogeti France \| Gérez la transformation numérique de votre entreprise avec Sogeti |
            | Germany       | Sogeti Deutschland GmbH – Beratungsdienstleistungen für Softwaretest und Qualitätssicherung |
            | Ireland       | Sogeti Ireland                    |
            | Luxembourg    | Sogeti Luxembourg                 |
            | Netherlands   | We Make Technology Work \| Sogeti |
            | Norway        | Sogeti Norge                      |
            | Spain         | Sogeti España                     |
            | Sweden        | Sogeti Sverige                    |
            | UK            | Sogeti UK \| Software Testing Services, Digital Services, DevOps Services, DevOps Consultancy, Testing Consultancy |
            | USA           | Sogeti USA                        |

