# Parts-unilimited

Parts-unlimited is a project written in Python/Django with a Sqlite database to store Parts and its properties as SKU, Weight (ounces) and description.
Github: ([https://github.com/t3rcio/parts-unlimited](https://github.com/t3rcio/parts-unlimited))

## Running the project
### Dev environment
To run the project in your dev environment you should install the Python Libs at your Python env.
([Read more about Python environments](https://docs.python.org/3/library/venv.html))

After activate your dev environement install the requirements:

    pip install -r requirements.txt

You can run the development server with:

    python app/manage.py runserver 0.0.0.0:8000 # choice your PORT

The tests can be executed with:

    python app/manage.py test

### Docking
To run the project in a container just execute the following command in the project's directory:

    docker-compose up --build -d

Finally, just point your browser to http://localhost:8000 and thats it. ;-)

## The RESTFull API

### Getting Parts
There is three ways of getting parts objects from this API:

#### **1: GET a list of parts:**
Performing a GET request at `/api/parts` will return you a list with all parts stored on database.

#### **2: GET a** _**specific**_ **part by SKU code:**
By performing a GET request at `/api/part/sku={sku}` you can get a specific part.

#### **3: GET a collection of parts by specifics params and values:**
It is possible to obtain a list with parts performing a GET request with *specific* params and values; using the endpoint `/api/part/param={param}/value={value}`
At the file `core/models.py` is possible to see the `SEARCH_FIELDS` variable wich one is part of the search mechanism.

#### Pagination
All the GET endpoints has a pagination mechanism. All you must do is to pass the page number on the querystring; 
Eg.:`/api/parts?page=[1,2,...N]` or `/api/parts/param=is_active/value=1?page=[1,2...N]`
The page size default is 50; it is possible to change this value at settings.py.
The result seems like this:
```json
{
	"items": [
		/*all_the_items_here*/
	],
	"pages": 24,
	"current_page": 24,
	"next_page": "",
	"previous_page": "/api/parts/param=weight_ounces/value=20?page=23"
}
```
### Creating a new Part

It is possible to create a new part by making a POST request at the endpoint `/api/part/new` sending a JSON object in the request's body:
```json
{  "name":  "some-name-part",  "sku":  "SOMESKUVALUE-456",  "description":  "A description text for the part",  "weight_onces":  100,  "is_active":  0  }
```

### Updating a Part

To update a part, make a request PUT at the `/api/part/sku={sku}`. In the request's body send the JSON object with the new values for the part.
```json
{  "name":  "some-name-part",  "sku":  "SOMESKUVALUE-456",  "description":  "A description text for the part",  "weight_onces":  100,  "is_active":  0  }
```
### Deleting a Part

Deleting a part is possible by making a DELETE request at the endpoint: `/api/part/sku={sku}`.
The *sku* value passed on the querystring is returned in a JSON object to confirm the object was removed successfully.

## For the Sales team
The Sales team can obtain the 5 most common words in the part's descriptions by performing a GET at the endpoint:

    /api/parts/mostcommonwords

wich return the result in JSON:
```json
   {    
    "ever": 49,
    "form": 32,
    "very": 29,
    "part": 27,
    "other": 27
   }
```
Besides that, it is possible to obtain the 5 most common words by part at the endpoint:

    /api/part/sku={sku}/mostcommonwords

It is possible to increase (or decrease) this number by chaning the variable WORDS_MOST_COMMON_LIMIT in the `core/views.py` file.