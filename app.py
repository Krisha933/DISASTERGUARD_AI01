from flask import Flask, render_template, jsonify, request, Response
import json
import urllib.request
import joblib
import urllib.parse
import os
from datetime import datetime


app = Flask(__name__)


# =========================================================
# FAVICON
# =========================================================

@app.route("/favicon.ico")
def favicon():
    return Response(status=204)


# =========================================================
# LOAD FLOOD MODEL
# =========================================================

model = joblib.load(
    "models/flood_model.pkl"
)


# =========================================================
# LOAD HISTORICAL DISASTER DATA
# =========================================================

with open(
    "data/historical_disasters.json",
    "r",
    encoding="utf-8"
) as file:

    historical_data = json.load(file)


# =========================================================
# 🆘 RELIEF FILE STORAGE
# =========================================================

RELIEF_FILE = os.path.join(
    os.path.dirname(__file__),
    "database",
    "relief_requests.json"
)


# =========================================================
# 🤝 VERIFIED HELPERS
# =========================================================

HELPERS_FILE = os.path.join(
    os.path.dirname(__file__),
    "database",
    "relief_helpers.json"
)


# =========================================================
# 💳 RELIEF SPONSORS
# =========================================================

SPONSORS_FILE = os.path.join(
    os.path.dirname(__file__),
    "database",
    "relief_sponsors.json"
)


# =========================================================
# RELIEF REQUEST FUNCTIONS
# =========================================================

def load_relief_requests():

    if not os.path.exists(
        RELIEF_FILE
    ):
        return []

    try:

        with open(
            RELIEF_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(
            data,
            list
        ):
            return data

        return []

    except (
        json.JSONDecodeError,
        OSError
    ):

        return []


def save_relief_requests(
    requests_list
):

    os.makedirs(
        os.path.dirname(
            RELIEF_FILE
        ),
        exist_ok=True
    )

    with open(
        RELIEF_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            requests_list,
            file,
            indent=4,
            ensure_ascii=False
        )


# =========================================================
# 🔎 FIND LATEST RELIEF REQUEST
# =========================================================

def find_relief_request(
    requests_list,
    request_id
):

    target_id = str(
        request_id
    ).strip()

    # Search from latest record first.
    # This protects against accidental duplicate
    # request IDs in the JSON database.

    for item in reversed(
        requests_list
    ):

        current_id = str(
            item.get(
                "request_id",
                ""
            )
        ).strip()

        if current_id == target_id:

            return item

    return None


# =========================================================
# VERIFIED HELPER FUNCTIONS
# =========================================================

def load_relief_helpers():

    if not os.path.exists(
        HELPERS_FILE
    ):
        return []

    try:

        with open(
            HELPERS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(
            data,
            list
        ):
            return data

        return []

    except (
        json.JSONDecodeError,
        OSError
    ):

        return []


# =========================================================
# SPONSOR FUNCTIONS
# =========================================================

def load_relief_sponsors():

    if not os.path.exists(
        SPONSORS_FILE
    ):
        return []

    try:

        with open(
            SPONSORS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(
            data,
            list
        ):
            return data

        return []

    except (
        json.JSONDecodeError,
        OSError
    ):

        return []


def save_relief_sponsors(
    sponsors_list
):

    os.makedirs(
        os.path.dirname(
            SPONSORS_FILE
        ),
        exist_ok=True
    )

    with open(
        SPONSORS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            sponsors_list,
            file,
            indent=4,
            ensure_ascii=False
        )


# =========================================================
# 🆘 CREATE EMERGENCY HELP REQUEST
# =========================================================

@app.route(
    "/api/relief/request",
    methods=["POST"]
)
def create_relief_request():

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "success": False,
                "message":
                    "No request data received."
            }), 400

        name = str(
            data.get(
                "name",
                ""
            )
        ).strip()

        phone = str(
            data.get(
                "phone",
                ""
            )
        ).strip()

        location = str(
            data.get(
                "location",
                ""
            )
        ).strip()

        people = data.get(
            "people",
            1
        )

        needs = data.get(
            "needs",
            []
        )

        emergency = str(
            data.get(
                "emergency",
                "Medium"
            )
        ).strip()

        message = str(
            data.get(
                "message",
                ""
            )
        ).strip()

        # -----------------------------
        # VALIDATION
        # -----------------------------

        if not name:

            return jsonify({
                "success": False,
                "message":
                    "Name is required."
            }), 400

        if not phone:

            return jsonify({
                "success": False,
                "message":
                    "Phone number is required."
            }), 400

        if not location:

            return jsonify({
                "success": False,
                "message":
                    "Location is required."
            }), 400

        if not needs:

            return jsonify({
                "success": False,
                "message":
                    "Please select at least one required item."
            }), 400

        # -----------------------------
        # PEOPLE
        # -----------------------------

        try:

            people = int(
                people
            )

            if people < 1:
                people = 1

        except (
            ValueError,
            TypeError
        ):

            people = 1

        # -----------------------------
        # EMERGENCY
        # -----------------------------

        allowed_emergency = [
            "Critical",
            "High",
            "Medium"
        ]

        if emergency not in allowed_emergency:

            emergency = "Medium"

        # -----------------------------
        # LOAD REQUESTS
        # -----------------------------

        requests_list = (
            load_relief_requests()
        )

        # -----------------------------
        # REQUEST ID
        # -----------------------------

        request_id = (
            "RELIEF-" +
            datetime.now().strftime(
                "%Y%m%d%H%M%S%f"
            )
        )

        # -----------------------------
        # REQUEST OBJECT
        # -----------------------------

        relief_request = {

            "request_id":
                request_id,

            "name":
                name,

            "phone":
                phone,

            "location":
                location,

            "people":
                people,

            "needs":
                needs,

            "emergency":
                emergency,

            "message":
                message,

            "status":
                "Pending",

            "sponsored":
                False,

            "helper_assigned":
                False,

            "created_at":
                datetime.now().isoformat()

        }

        requests_list.append(
            relief_request
        )

        save_relief_requests(
            requests_list
        )

        return jsonify({

            "success":
                True,

            "message":
                "Emergency help request submitted successfully.",

            "request":
                relief_request

        }), 201

    except Exception as error:

        print(
            "Relief Request Error:",
            error
        )

        return jsonify({

            "success":
                False,

            "message":
                "Unable to create help request."

        }), 500


# =========================================================
# 📊 HISTORICAL RISK
# =========================================================

def get_historical_risk(
    city
):

    records = [

        record

        for record in historical_data

        if record[
            "city"
        ].lower()
        ==
        city.lower()

    ]

    if not records:

        return {

            "score":
                0,

            "level":
                "LOW",

            "incidents":
                0

        }

    incidents = len(
        records
    )

    high_severity = sum(

        1

        for record in records

        if record[
            "severity"
        ]
        ==
        "High"

    )

    medium_severity = sum(

        1

        for record in records

        if record[
            "severity"
        ]
        ==
        "Medium"

    )

    score = (
        incidents * 10
        + high_severity * 10
        + medium_severity * 5
    )

    score = min(
        score,
        100
    )

    if score < 25:

        level = "LOW"

    elif score < 50:

        level = "MEDIUM"

    elif score < 75:

        level = "HIGH"

    else:

        level = "CRITICAL"

    return {

        "score":
            score,

        "level":
            level,

        "incidents":
            incidents

    }


# =========================================================
# HISTORICAL RISK API
# =========================================================

@app.route(
    "/historical-risk"
)
def historical_risk_api():

    city = request.args.get(
        "city",
        ""
    )

    result = get_historical_risk(
        city
    )

    return jsonify({

        "city":
            city,

        "historical_risk":
            result

    })


# =========================================================
# 🌊 FLOOD PREDICTION
# =========================================================

@app.route(
    "/predict-flood",
    methods=["GET"]
)
def predict_flood():

    try:

        temperature = float(
            request.args.get(
                "temperature",
                25
            )
        )

        rainfall = float(
            request.args.get(
                "rainfall",
                0
            )
        )

        wind = float(
            request.args.get(
                "wind",
                10
            )
        )

        prediction = model.predict([
            [
                temperature,
                rainfall,
                wind
            ]
        ])[0]

        probability = model.predict_proba([
            [
                temperature,
                rainfall,
                wind
            ]
        ])[0][1]

        if prediction == 1:

            result = "FLOOD RISK"

        else:

            result = "NORMAL"

        return jsonify({

            "prediction":
                int(prediction),

            "result":
                result,

            "probability":
                round(
                    float(
                        probability
                    ) * 100,
                    2
                ),

            "temperature":
                temperature,

            "rainfall":
                rainfall,

            "wind":
                wind

        })

    except Exception as error:

        print(
            "Flood Prediction Error:",
            error
        )

        return jsonify({

            "success":
                False,

            "message":
                "Unable to predict flood risk."

        }), 500


# =========================================================
# 🛡️ SAFE ROUTE ANALYSIS
# =========================================================

@app.route(
    "/safe-route"
)
def safe_route():

    try:

        latitude = float(
            request.args.get(
                "latitude",
                0
            )
        )

        longitude = float(
            request.args.get(
                "longitude",
                0
            )
        )

        destination = request.args.get(
            "destination",
            ""
        ).strip()

        risk = float(
            request.args.get(
                "risk",
                0
            )
        )

        flood = float(
            request.args.get(
                "flood",
                0
            )
        )

        lightning = float(
            request.args.get(
                "lightning",
                0
            )
        )

        storm = float(
            request.args.get(
                "storm",
                0
            )
        )

        weather = float(
            request.args.get(
                "weather",
                0
            )
        )

        if not destination:

            return jsonify({

                "success":
                    False,

                "message":
                    "Destination is required"

            }), 400

        hazards = {

            "Flood":
                flood,

            "Lightning":
                lightning,

            "Storm":
                storm,

            "Severe Weather":
                weather

        }

        highest_hazard = max(
            hazards,
            key=hazards.get
        )

        highest_hazard_risk = hazards[
            highest_hazard
        ]

        if risk >= 75:

            route_status = "CRITICAL"

            recommendation = (
                "Avoid unnecessary travel. "
                "Move to a safer location and "
                "follow official emergency instructions."
            )

        elif risk >= 50:

            route_status = "HIGH RISK"

            recommendation = (
                f"High {highest_hazard} risk detected. "
                "Avoid unnecessary travel and "
                "high-risk areas."
            )

        elif risk >= 25:

            route_status = "CAUTION"

            recommendation = (
                f"Moderate {highest_hazard} risk detected. "
                "Travel with caution and avoid "
                "low-lying, waterlogged or exposed areas."
            )

        else:

            route_status = "LOW RISK"

            recommendation = (
                "Current environmental conditions "
                "are relatively safe for travel. "
                "Continue monitoring live alerts."
            )

        if (
            highest_hazard == "Flood"
            and flood >= 25
        ):

            recommendation += (
                " Avoid waterlogged roads, "
                "drainage areas and low-lying locations."
            )

        elif (
            highest_hazard == "Lightning"
            and lightning >= 25
        ):

            recommendation += (
                " Avoid open areas and exposed locations "
                "during thunder or lightning activity."
            )

        elif (
            highest_hazard == "Storm"
            and storm >= 25
        ):

            recommendation += (
                " Avoid exposed roads and "
                "areas with strong wind conditions."
            )

        elif (
            highest_hazard == "Severe Weather"
            and weather >= 25
        ):

            recommendation += (
                " Monitor weather alerts before "
                "starting your journey."
            )

        return jsonify({

            "success":
                True,

            "destination":
                destination,

            "overall_risk":
                round(
                    risk,
                    1
                ),

            "highest_hazard":
                highest_hazard,

            "highest_hazard_risk":
                round(
                    highest_hazard_risk,
                    1
                ),

            "route_status":
                route_status,

            "recommendation":
                recommendation,

            "origin": {

                "latitude":
                    latitude,

                "longitude":
                    longitude

            }

        })

    except Exception as error:

        print(
            "Safe Route Error:",
            error
        )

        return jsonify({

            "success":
                False,

            "message":
                "Unable to analyse safe route"

        }), 500


# =========================================================
# 🛣️ ROUTE RISK COMPARISON
# =========================================================

@app.route(
    "/compare-routes",
    methods=["GET"]
)
def compare_routes():

    try:

        latitude = float(
            request.args.get(
                "latitude"
            )
        )

        longitude = float(
            request.args.get(
                "longitude"
            )
        )

        destination = request.args.get(
            "destination",
            ""
        ).strip()

        overall_risk = float(
            request.args.get(
                "risk",
                0
            )
        )

        flood_risk = float(
            request.args.get(
                "flood",
                0
            )
        )

        lightning_risk = float(
            request.args.get(
                "lightning",
                0
            )
        )

        storm_risk = float(
            request.args.get(
                "storm",
                0
            )
        )

        weather_risk = float(
            request.args.get(
                "weather",
                0
            )
        )

        if not destination:

            return jsonify({

                "success":
                    False,

                "message":
                    "Destination is required"

            }), 400

        # -----------------------------------------
        # GEOCODE DESTINATION
        # -----------------------------------------

        query = urllib.parse.quote(
            destination
        )

        geocode_url = (
            "https://nominatim.openstreetmap.org/search"
            "?format=json"
            "&limit=1"
            "&q=" +
            query
        )

        req = urllib.request.Request(
            geocode_url,
            headers={
                "User-Agent":
                    "DisasterGuardAI/1.0"
            }
        )

        with urllib.request.urlopen(
            req,
            timeout=10
        ) as response:

            location_data = json.loads(
                response
                .read()
                .decode("utf-8")
            )

        if not location_data:

            return jsonify({

                "success":
                    False,

                "message":
                    "Destination not found"

            }), 404

        destination_lat = float(
            location_data[0]["lat"]
        )

        destination_lon = float(
            location_data[0]["lon"]
        )

        # -----------------------------------------
        # GET ROUTES
        # -----------------------------------------

        route_url = (
            "https://router.project-osrm.org/"
            "route/v1/driving/"
            f"{longitude},{latitude};"
            f"{destination_lon},{destination_lat}"
            "?overview=full"
            "&geometries=geojson"
            "&alternatives=true"
        )

        route_request = urllib.request.Request(
            route_url,
            headers={
                "User-Agent":
                    "DisasterGuardAI/1.0"
            }
        )

        with urllib.request.urlopen(
            route_request,
            timeout=15
        ) as response:

            route_data = json.loads(
                response
                .read()
                .decode("utf-8")
            )

        if route_data.get(
            "code"
        ) != "Ok":

            return jsonify({

                "success":
                    False,

                "message":
                    "Unable to find routes"

            }), 500

        routes = route_data.get(
            "routes",
            []
        )

        if not routes:

            return jsonify({

                "success":
                    False,

                "message":
                    "No route found"

            }), 404

        # -----------------------------------------
        # CALCULATE ROUTE RISK
        # -----------------------------------------

        results = []

        base_hazard_risk = (
            (flood_risk * 0.35)
            +
            (storm_risk * 0.25)
            +
            (lightning_risk * 0.20)
            +
            (weather_risk * 0.20)
        )

        shortest_distance = min(
            route["distance"]
            for route in routes
        )

        for index, route in enumerate(
            routes
        ):

            distance_km = (
                route["distance"]
                /
                1000
            )

            duration_minutes = (
                route["duration"]
                /
                60
            )

            distance_factor = (
                distance_km
                /
                max(
                    shortest_distance / 1000,
                    1
                )
            )

            exposure_factor = min(
                distance_factor * 5,
                15
            )

            route_risk = min(
                round(
                    (
                        base_hazard_risk
                        *
                        0.85
                    )
                    +
                    exposure_factor
                ),
                100
            )

            results.append({

                "route_number":
                    index + 1,

                "distance_km":
                    round(
                        distance_km,
                        2
                    ),

                "duration_minutes":
                    round(
                        duration_minutes
                    ),

                "risk_score":
                    route_risk,

                "geometry":
                    route.get(
                        "geometry",
                        {}
                    )

            })

        recommended_route = min(
            results,
            key=lambda route:
                route["risk_score"]
        )

        for route in results:

            route["recommended"] = (

                route["route_number"]
                ==
                recommended_route[
                    "route_number"
                ]

            )

        return jsonify({

            "success":
                True,

            "destination":
                destination,

            "destination_coordinates": {

                "latitude":
                    destination_lat,

                "longitude":
                    destination_lon

            },

            "overall_risk":
                round(
                    overall_risk,
                    2
                ),

            "routes":
                results,

            "recommended_route":
                recommended_route[
                    "route_number"
                ],

            "analysis":
                (
                    "Routes are compared using "
                    "estimated multi-hazard risk "
                    "and route exposure."
                )

        })

    except Exception as error:

        print(
            "Route Comparison Error:",
            error
        )

        return jsonify({

            "success":
                False,

            "message":
                "Unable to compare routes"

        }), 500


# =========================================================
# 🆘 GET RELIEF REQUESTS
# =========================================================

@app.route(
    "/api/relief/requests",
    methods=["GET"]
)
def get_relief_requests():

    try:

        requests_list = (
            load_relief_requests()
        )

        return jsonify({

            "success":
                True,

            "requests":
                requests_list

        })

    except Exception as error:

        print(
            "Relief Requests Error:",
            error
        )

        return jsonify({

            "success":
                False,

            "message":
                "Unable to load relief requests."

        }), 500


# =========================================================
# 🤝 FIND VERIFIED HELPERS
# =========================================================

@app.route(
    "/api/relief/helpers/<request_id>",
    methods=["GET"]
)
def get_relief_helpers(
    request_id
):

    try:

        requests_list = (
            load_relief_requests()
        )

        # IMPORTANT:
        # Always use latest matching request.

        relief_request = (
            find_relief_request(
                requests_list,
                request_id
            )
        )

        if relief_request is None:

            return jsonify({

                "success":
                    False,

                "message":
                    "Relief request not found."

            }), 404

        helpers = (
            load_relief_helpers()
        )

        required_needs = set(
            relief_request.get(
                "needs",
                []
            )
        )

        matched_helpers = []

        for helper in helpers:

            if not helper.get(
                "verified",
                False
            ):
                continue

            if helper.get(
                "status"
            ) != "Available":
                continue

            helper_services = set(
                helper.get(
                    "services",
                    []
                )
            )

            matched_needs = list(
                required_needs.intersection(
                    helper_services
                )
            )

            pending_needs = list(
                required_needs.difference(
                    helper_services
                )
            )

            if matched_needs:

                helper_copy = dict(
                    helper
                )

                helper_copy[
                    "matched_needs"
                ] = matched_needs

                helper_copy[
                    "pending_needs"
                ] = pending_needs

                helper_copy[
                    "match_count"
                ] = len(
                    matched_needs
                )

                helper_copy[
                    "total_required"
                ] = len(
                    required_needs
                )

                matched_helpers.append(
                    helper_copy
                )

        matched_helpers.sort(
            key=lambda helper: (
                -helper.get(
                    "match_count",
                    0
                ),
                helper.get(
                    "distance_km",
                    999
                )
            )
        )

        return jsonify({

            "success":
                True,

            "request":
                relief_request,

            "helpers":
                matched_helpers

        })

    except Exception as error:

        print(
            "Helper Matching Error:",
            error
        )

        return jsonify({

            "success":
                False,

            "message":
                "Unable to find nearby helpers."

        }), 500


# =========================================================
# 🤝 ACCEPT RELIEF REQUEST
# =========================================================

@app.route(
    "/api/relief/request/<request_id>/accept",
    methods=["POST"]
)
def accept_relief_request(
    request_id
):

    try:

        data = (
            request.get_json()
            or {}
        )

        helper_id = str(
            data.get(
                "helper_id",
                ""
            )
        ).strip()

        if not helper_id:

            return jsonify({

                "success":
                    False,

                "message":
                    "Helper ID is required."

            }), 400

        requests_list = (
            load_relief_requests()
        )

        helpers = (
            load_relief_helpers()
        )

        # Use latest matching request.

        relief_request = (
            find_relief_request(
                requests_list,
                request_id
            )
        )

        if relief_request is None:

            return jsonify({

                "success":
                    False,

                "message":
                    "Relief request not found."

            }), 404

        helper = None

        for item in helpers:

            if (
                str(
                    item.get(
                        "helper_id",
                        ""
                    )
                ).strip()
                ==
                helper_id
            ):

                helper = item
                break

        if helper is None:

            return jsonify({

                "success":
                    False,

                "message":
                    "Helper not found."

            }), 404

        if not helper.get(
            "verified",
            False
        ):

            return jsonify({

                "success":
                    False,

                "message":
                    "Only verified helpers can accept requests."

            }), 403

        if (
            relief_request.get(
                "status"
            )
            !=
            "Pending"
        ):

            return jsonify({

                "success":
                    False,

                "message":
                    "This request is no longer available."

            }), 409

        relief_request[
            "status"
        ] = "Helper Assigned"

        relief_request[
            "helper_assigned"
        ] = True

        relief_request[
            "helper_id"
        ] = helper.get(
            "helper_id"
        )

        relief_request[
            "helper_name"
        ] = helper.get(
            "name"
        )

        relief_request[
            "helper_type"
        ] = helper.get(
            "type"
        )

        relief_request[
            "helper_phone"
        ] = helper.get(
            "phone"
        )

        relief_request[
            "assigned_at"
        ] = datetime.now().isoformat()

        save_relief_requests(
            requests_list
        )

        return jsonify({

            "success":
                True,

            "message":
                "Relief request accepted successfully.",

            "request":
                relief_request,

            "helper":
                helper

        })

    except Exception as error:

        print(
            "Accept Relief Error:",
            error
        )

        return jsonify({

            "success":
                False,

            "message":
                "Unable to accept relief request."

        }), 500


# =========================================================
# 🚚 START RELIEF DELIVERY
# =========================================================

@app.route(
    "/api/relief/request/<request_id>/start",
    methods=["POST"]
)
def start_relief_delivery(
    request_id
):

    try:

        data = (
            request.get_json()
            or {}
        )

        helper_id = str(
            data.get(
                "helper_id",
                ""
            )
        ).strip()

        if not helper_id:

            return jsonify({

                "success":
                    False,

                "message":
                    "Helper ID is required."

            }), 400

        requests_list = (
            load_relief_requests()
        )

        # IMPORTANT:
        # Use latest matching request.

        relief_request = (
            find_relief_request(
                requests_list,
                request_id
            )
        )

        if relief_request is None:

            return jsonify({

                "success":
                    False,

                "message":
                    "Relief request not found."

            }), 404

        stored_helper_id = str(
            relief_request.get(
                "helper_id",
                ""
            )
        ).strip()

        if stored_helper_id != helper_id:

            return jsonify({

                "success":
                    False,

                "message":
                    "Only the assigned helper can start delivery."

            }), 403

        current_status = str(
            relief_request.get(
                "status",
                ""
            )
        ).strip()

        if current_status != "Helper Assigned":

            return jsonify({

                "success":
                    False,

                "message":
                    "Request must be Helper Assigned before delivery starts.",

                "current_status":
                    current_status

            }), 409

        relief_request[
            "status"
        ] = "In Progress"

        relief_request[
            "delivery_started_at"
        ] = datetime.now().isoformat()

        save_relief_requests(
            requests_list
        )

        return jsonify({

            "success":
                True,

            "message":
                "Relief delivery started successfully.",

            "request":
                relief_request

        })

    except Exception as error:

        print(
            "Start Delivery Error:",
            error
        )

        return jsonify({

            "success":
                False,

            "message":
                "Unable to start relief delivery."

        }), 500


# =========================================================
# 🟢 MARK RELIEF AS DELIVERED
# =========================================================

@app.route(
    "/api/relief/request/<request_id>/delivered",
    methods=["POST"]
)
def mark_relief_delivered(
    request_id
):

    try:

        data = (
            request.get_json()
            or {}
        )

        helper_id = str(
            data.get(
                "helper_id",
                ""
            )
        ).strip()

        if not helper_id:

            return jsonify({

                "success":
                    False,

                "message":
                    "Helper ID is required."

            }), 400

        requests_list = (
            load_relief_requests()
        )

        # IMPORTANT:
        # Always select latest request.

        relief_request = (
            find_relief_request(
                requests_list,
                request_id
            )
        )

        if relief_request is None:

            return jsonify({

                "success":
                    False,

                "message":
                    "Relief request not found."

            }), 404

        stored_helper_id = str(
            relief_request.get(
                "helper_id",
                ""
            )
        ).strip()

        if stored_helper_id != helper_id:

            return jsonify({

                "success":
                    False,

                "message":
                    "Only the assigned helper can mark delivery."

            }), 403

        current_status = str(
            relief_request.get(
                "status",
                ""
            )
        ).strip()

        # -------------------------------------------------
        # DELIVERY MUST BE IN PROGRESS
        # -------------------------------------------------

        if current_status != "In Progress":

            return jsonify({

                "success":
                    False,

                "message":
                    "Delivery must be In Progress first.",

                "current_status":
                    current_status,

                "request_id":
                    request_id,

                "helper_id":
                    stored_helper_id

            }), 409

        # -------------------------------------------------
        # MARK DELIVERED
        # -------------------------------------------------

        relief_request[
            "status"
        ] = "Delivered"

        relief_request[
            "delivered_at"
        ] = datetime.now().isoformat()

        relief_request[
            "delivery_completed"
        ] = True

        save_relief_requests(
            requests_list
        )

        return jsonify({

            "success":
                True,

            "message":
                "Relief delivered successfully.",

            "request":
                relief_request

        })

    except Exception as error:

        print(
            "Mark Delivered Error:",
            error
        )

        return jsonify({

            "success":
                False,

            "message":
                "Unable to mark relief as delivered."

        }), 500


# =========================================================
# 💳 SPONSOR RELIEF REQUEST
# =========================================================

@app.route(
    "/api/relief/request/<request_id>/sponsor",
    methods=["POST"]
)
def sponsor_relief_request(
    request_id
):

    try:

        data = (
            request.get_json()
            or {}
        )

        sponsor_name = str(
            data.get(
                "sponsor_name",
                ""
            )
        ).strip()

        amount = data.get(
            "amount",
            0
        )

        if not sponsor_name:

            return jsonify({

                "success":
                    False,

                "message":
                    "Sponsor name is required."

            }), 400

        try:

            amount = float(
                amount
            )

        except (
            ValueError,
            TypeError
        ):

            amount = 0

        if amount <= 0:

            return jsonify({

                "success":
                    False,

                "message":
                    "Enter a valid sponsorship amount."

            }), 400

        requests_list = (
            load_relief_requests()
        )

        # Use latest request.

        relief_request = (
            find_relief_request(
                requests_list,
                request_id
            )
        )

        if relief_request is None:

            return jsonify({

                "success":
                    False,

                "message":
                    "Relief request not found."

            }), 404

        sponsors = (
            load_relief_sponsors()
        )

        sponsor_id = (
            "SPONSOR-" +
            datetime.now().strftime(
                "%Y%m%d%H%M%S%f"
            )
        )

        sponsor = {

            "sponsor_id":
                sponsor_id,

            "request_id":
                request_id,

            "sponsor_name":
                sponsor_name,

            "amount":
                round(
                    amount,
                    2
                ),

            "status":
                "Confirmed",

            "created_at":
                datetime.now().isoformat()

        }

        sponsors.append(
            sponsor
        )

        save_relief_sponsors(
            sponsors
        )

        relief_request[
            "sponsored"
        ] = True

        relief_request[
            "sponsored_amount"
        ] = round(
            amount,
            2
        )

        relief_request[
            "sponsor_name"
        ] = sponsor_name

        relief_request[
            "sponsor_id"
        ] = sponsor_id

        relief_request[
            "sponsor_status"
        ] = "Confirmed"

        save_relief_requests(
            requests_list
        )

        return jsonify({

            "success":
                True,

            "message":
                "Relief request sponsored successfully.",

            "sponsor":
                sponsor,

            "request":
                relief_request

        })

    except Exception as error:

        print(
            "Sponsor Relief Error:",
            error
        )

        return jsonify({

            "success":
                False,

            "message":
                "Unable to sponsor relief request."

        }), 500


# =========================================================
# 🏠 HOME
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# 📍 LOCATION SEARCH / GEOCODE
# =========================================================

@app.route(
    "/geocode"
)
def geocode():

    location = request.args.get(
        "q",
        ""
    ).strip()

    if not location:

        return jsonify({

            "success":
                False,

            "message":
                "Location is required"

        }), 400

    try:

        query = urllib.parse.quote(
            location
        )

        url = (
            "https://nominatim.openstreetmap.org/search"
            "?format=json"
            "&limit=1"
            "&addressdetails=1"
            "&q=" +
            query
        )

        req = urllib.request.Request(
            url,
            headers={
                "User-Agent":
                    "DisasterGuardAI/1.0"
            }
        )

        with urllib.request.urlopen(
            req,
            timeout=10
        ) as response:

            data = json.loads(
                response
                .read()
                .decode("utf-8")
            )

        if not data:

            return jsonify({

                "success":
                    False,

                "message":
                    "Location not found"

            })

        result = data[0]

        return jsonify({

            "success":
                True,

            "latitude":
                float(
                    result["lat"]
                ),

            "longitude":
                float(
                    result["lon"]
                ),

            "display_name":
                result.get(
                    "display_name",
                    location
                ),

            "address":
                result.get(
                    "address",
                    {}
                )

        })

    except Exception as error:

        print(
            "Geocoding Error:",
            error
        )

        return jsonify({

            "success":
                False,

            "message":
                "Unable to search location"

        }), 500


# =========================================================
# 🚀 START FLASK
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )