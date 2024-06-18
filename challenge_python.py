import requests
import boto3

"""
Refactor the next function using yield to return the array of objects found by the
`s3.list_objects_v2` function that matches the given prefix.
"""


def get_s3_objects(bucket, prefix=""):
    s3 = boto3.client("s3")

    kwargs = {"Bucket": bucket}
    next_token = None
    if prefix:
        kwargs["Prefix"] = prefix
    while True:
        if next_token:
            kwargs["ContinuationToken"] = next_token
        resp = s3.list_objects_v2(**kwargs)
        contents = resp.get("Contents", [])
        for obj in contents:
            key = obj["Key"]
            if key.startswith(prefix):
                yield obj
        next_token = resp.get("NextContinuationToken", None)

        if not next_token:
            break


"""
Please, full explain this function: document iterations, conditionals, and the
function as a whole
"""


def fn(main_plan, obj, extensions=[]) -> list:
    """
    Process the main plan and extensions to generate a list of items.

    Args:
        main_plan (object): The main plan object.
        obj (object): The object containing items data.
        extensions (list, optional): The list of extension objects. Defaults to [].

    Returns:
        list: The list of items, including the main plan and extensions.

    """
    items = []  # Create an empty list to store the items

    sp = False  # Initialize a flag variable for the main plan
    cd = False  # Initialize a flag variable for deleted items

    ext_p = {}  # Create an empty dictionary to store the extension prices

    # Iterate over each extension and store the price and quantity in the dictionary
    for ext in extensions:
        ext_p[ext["price"].id] = ext["qty"]

    # Iterate over each item in the object's data
    for item in obj["items"].data:
        product = {
            "id": item.id
        }  # Create a dictionary to store the product information

        # Check if the item's price is not the main plan and not in the extension prices
        if item.price.id != main_plan.id and item.price.id not in ext_p:
            product["deleted"] = True  # Mark the product as deleted
            cd = True  # Set the deleted flag to True
        # Check if the item's price is in the extension prices
        elif item.price.id in ext_p:
            qty = ext_p[item.price.id]  # Get the quantity from the extension prices
            if qty < 1:
                product["deleted"] = True  # Mark the product as deleted
            else:
                product["qty"] = qty  # Set the quantity for the product
            del ext_p[item.price.id]  # Remove the price from the extension prices
        # Check if the item's price is the main plan
        elif item.price.id == main_plan.id:
            sp = True  # Set the main plan flag to True

        items.append(product)  # Add the product to the items list

    # Check if the main plan is not included in the items list
    if not sp:
        items.append(
            {"id": main_plan.id, "qty": 1}
        )  # Add the main plan to the items list with quantity 1

    # Iterate over the remaining extension prices in the extension prices dictionary
    for price, qty in ext_p.items():
        if qty < 1:
            continue
        items.append(
            {"id": price, "qty": qty}
        )  # Add the extension price to the items list with the corresponding quantity

    return items  # Return the items list


"""
Having the class `Caller` and the function `fn`
Refactor the function `fn` to execute any method from `Caller` using the argument `fn_to_call`
reducing the `fn` function to only one line.
"""


class Caller:
    add = lambda a, b: a + b
    concat = lambda a, b: f"{a},{b}"
    divide = lambda a, b: a / b
    multiply = lambda a, b: a * b


def fn(fn_to_call, *args):
    # Just in case the method does not exist
    if not hasattr(Caller, fn_to_call):
        return None

    func = getattr(Caller, fn_to_call)  # Get the method
    result = func(*args)  # Execute it

    return result


"""
A video transcoder was implemented with different presets to process different videos in the application. The videos should be
encoded with a given configuration done by this function. Can you explain what this function is detecting from the params
and returning based in its conditionals?
"""


def fn(config, w, h):
    """
    Returns the appropriate preset based on the video aspect ratio

    Args:
        config (dict): A dictionary containing configuration data.
        w (int): The video width.
        h (int): The video height.

    Returns:
        list: All the presets for the respective mode with matching width.
    """
    # This variable will store the selected preset based on
    # the aspect ratio of the video. Default is None.
    v = None
    # Calculate the video's aspect ratio
    ar = w / h

    # Get all the presets for the respective
    # mode with width <= the given width "w".
    if ar < 1:  # Portrait mode: "p"
        v = [r for r in config["p"] if r["width"] <= w]
    elif ar > 4 / 3:  # Landscape mode: "l"
        v = [r for r in config["l"] if r["width"] <= w]
    else:  # Square mode: "s"
        v = [r for r in config["s"] if r["width"] <= w]

    return v  # Return the selected preset


"""
Having the next helper, please implement a refactor to perform the API call using one method instead of rewriting the code
in the other methods.
"""


class Helper:
    DOMAIN = "http://example.com"

    AUTHORIZATION_TOKEN = {
        "access_token": None,
        "token_type": None,
        "expires_in": 0,
        "refresh_token": None,
    }

    def _api_call(
        self,
        method: str,
        endpoint: str,
        **kwargs,
    ) -> requests.Response:
        token_type = self.AUTHORIZATION_TOKEN["token_type"]
        access_token = self.AUTHORIZATION_TOKEN["access_token"]

        headers = {
            "Authorization": f"{token_type} {access_token}",
        }

        url = f"{self.DOMAIN}{endpoint}"

        send = {"headers": headers, **kwargs}

        response = requests.request(method, url, **send)
        return response

    def search_images(self, **kwargs) -> requests.Response:
        return self._api_call(
            "get",
            "/search/images",
            params=kwargs,
        )

    def get_image(self, image_id, **kwargs) -> requests.Response:
        return self._api_call(
            "get",
            f"/image/{image_id}",
            params=kwargs,
        )

    def download_image(self, image_id, **kwargs) -> requests.Response:
        return self._api_call(
            "post",
            f"/downloads/images/{image_id}",
            data=kwargs,
        )
