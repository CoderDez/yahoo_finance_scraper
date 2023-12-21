import re


def float_formatter(value) -> float | None:
    cleaned_price = re.sub(r'[^\d.]', '', value)
    return float(cleaned_price) if cleaned_price else None

def display_dict(value: dict) -> str:
    try:
        output = ""
        for key in value:
            output += f"{key}\n"
            
            for k, v in value[key].items():
                output += f"{k}: {v}\n"

            output += "\n"

        return output

    except Exception as e:
        print("ERROR occurred while trying to display dict: ", e)
