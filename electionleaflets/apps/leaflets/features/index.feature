Feature: Leaflet uploader
    Scenario: Upload single image leaflet
        Given I access the url "/leaflets/add/front/"
        Then I see the header "Step 1: Front page"
        Then I submit the form with:
          | step_name | image          |  action |
          | front     | front_test.jpg |  submit |
        Then I submit the form with:
          | step_name | image          |  action |
          | back     |                 |  skip |
        Then I submit the form with:
          | step_name | postcode          |  action |
          | postcode  | SE22 8DJ          |  submit |
        Then I submit the form with:
          | step_name | people          |  action |
          | people    | None          |  submit |
        Then I should see the leaflet url
        and I should see 1 leaflet images
        in the constituency "Camberwell and Peckham"

    Scenario: Upload front and back
        Given I access the url "/leaflets/add/front/"
        Then I see the header "Step 1: Front page"
        Then I submit the form with:
          | step_name | image          |  action |
          | front     | front_test.jpg |  submit |
        Then I submit the form with:
          | step_name | image          |  action |
          | back     |  back_test.jpg  |  submit |
        Then I submit the form with:
          | step_name | image          |  action |
          | inside    |                |  skip |
        Then I submit the form with:
          | step_name | postcode          |  action |
          | postcode  | SE22 8DJ          |  submit |
        Then I submit the form with:
          | step_name | people          |  action |
          | people    | None          |  submit |
        Then I should see the leaflet url
        and I should see 2 leaflet images

    Scenario: Upload front, back and inside
        Given I access the url "/leaflets/add/front/"
        Then I see the header "Step 1: Front page"
        Then I submit the form with:
          | step_name | image           |  action |
          | front     | front_test.jpg  |  submit |
        Then I submit the form with:
          | step_name | image           |  action |
          | back     |  back_test.jpg   |  submit |
        Then I submit the form with:
          | step_name | image           |  action |
          | inside    | inside_test.jpg |  submit |
        Then I submit the form with:
          | step_name | postcode        |  action |
          | postcode  | SE22 8DJ        |  submit |
        Then I submit the form with:
          | step_name | people          |  action |
          | people    | None          |  submit |
        Then I should see the leaflet url
        and I should see 3 leaflet images

    Scenario: Upload front, back and two inside pages
        Given I access the url "/leaflets/add/front/"
        Then I see the header "Step 1: Front page"
        Then I submit the form with:
          | step_name | image           |  action |
          | front     | front_test.jpg  |  submit |
        Then I submit the form with:
          | step_name | image           |  action |
          | back     |  back_test.jpg   |  submit |
        Then I submit the form with:
          | step_name | image           |  action |
          | inside    | inside_test.jpg |  add_extra_inside |
        Then I submit the form with:
          | step_name | image           |  action |
          | inside-0    | inside_test.jpg |  submit |
        Then I submit the form with:
          | step_name | postcode        |  action |
          | postcode  | SE22 8DJ        |  submit |
        Then I submit the form with:
          | step_name | people          |  action |
          | people    | None          |  submit |
        Then I should see the leaflet url
        and I should see 4 leaflet images



    Scenario: Upload front, back and three inside pages
        Given I access the url "/leaflets/add/front/"
        Then I see the header "Step 1: Front page"
        Then I submit the form with:
          | step_name | image           |  action |
          | front     | front_test.jpg  |  submit |
        Then I submit the form with:
          | step_name | image           |  action |
          | back     |  back_test.jpg   |  submit |
        Then I submit the form with:
          | step_name | image           |  action |
          | inside    | inside_test.jpg |  add_extra_inside |
        Then I submit the form with:
          | step_name | image           |  action |
          | inside-0    | inside_test.jpg |  add_extra_inside |
        Then I submit the form with:
          | step_name | image           |  action |
          | inside-1    | inside_test.jpg |  skip |
        Then I submit the form with:
          | step_name | postcode        |  action |
          | postcode  | SE22 8DJ        |  submit |
        Then I submit the form with:
          | step_name | people          |  action |
          | people    | None          |  submit |
        Then I should see the url "/leaflets/5/"
        and I should see 5 leaflet images

    Scenario: Upload front, back and three inside pages, pressing 'no more pages'
        Given I access the url "/leaflets/add/front/"
        Then I see the header "Step 1: Front page"
        Then I submit the form with:
          | step_name | image           |  action |
          | front     | front_test.jpg  |  submit |
        Then I submit the form with:
          | step_name | image           |  action |
          | back     |  back_test.jpg   |  submit |
        Then I submit the form with:
          | step_name | image           |  action |
          | inside    | inside_test.jpg |  add_extra_inside |
        Then I submit the form with:
          | step_name | image           |  action |
          | inside-0    | inside_test.jpg |  add_extra_inside |
        Then I submit the form with:
          | step_name | image           |  action |
          | inside-1    | inside_test.jpg |  add_extra_inside |
        Then I submit the form with:
          | step_name | image           |  action |
          | inside-2    |  |  skip |
        Then I submit the form with:
          | step_name | postcode        |  action |
          | postcode  | SE22 8DJ        |  submit |
        Then I submit the form with:
          | step_name | people          |  action |
          | people    | None          |  submit |
        Then I should see the url "/leaflets/6/"
        and I should see 5 leaflet images

    Scenario: Upload single image leaflet with partial postcode
        Given I access the url "/leaflets/add/front/"
        Then I see the header "Step 1: Front page"
        Then I submit the form with:
          | step_name | image          |  action |
          | front     | front_test.jpg |  submit |
        Then I submit the form with:
          | step_name | image          |  action |
          | back     |                 |  skip |
        Then I submit the form with:
          | step_name | postcode          |  action |
          | postcode  | SE22          |  submit |
        Then I should see the url "/leaflets/add/postcode/"

    Scenario: Upload single image leaflet with non-existant postcode
        Given I access the url "/leaflets/add/front/"
        Then I see the header "Step 1: Front page"
        Then I submit the form with:
          | step_name | image          |  action |
          | front     | front_test.jpg |  submit |
        Then I submit the form with:
          | step_name | image          |  action |
          | back     |                 |  skip |
        Then I submit the form with:
          | step_name | postcode          |  action |
          | postcode  | SE22 3DJ          |  submit |
        Then I should see the url "/leaflets/add/postcode/"

