# %%
# Import necessary libraries
import os
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from collections import OrderedDict

# %%
def send_get_request(url):
    response = requests.get(url)
    return response


def parse_builder_details(url):
    builder_data = {}
    response = send_get_request(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # basic information
    builder_name = soup.find('h1', class_="css-14yp330").text 


    # description
    description_obj = soup.find('div', class_="css-fwetmj")
    builder_description = description_obj.text if description_obj else builder_name

    builder_info_obj_list = soup.find('div', class_="_i8mpn6wy _l86nkx _gzxlgz _j61wqb _9s1txw stats")

    establishment_info_dict = {}
    children = builder_info_obj_list.findChildren("div" , recursive=False)
    for obj in children:
        key = obj.find('div', class_="_c8dlk8 _1q73uea4").text.strip()
        value = obj.find('div', class_="_7l1r05").text.strip()
        establishment_info_dict.update({key: value})
    

    # icon
    icon_link_div = ""
    icon_link_div = soup.find(
        "div", class_="_mkstnw _fqexct _tkgktf _vy1rbs _e21rbs _5j1ssb _1ct41mtk _13vx1ul9 _lonopsqy thumbnail-wrapper"
        )
    if icon_link_div:
        icon_link = icon_link_div.find("img")
        if icon_link:
            icon_link = icon_link.get("src")
    

    builder_data = {
        "Builder Name": builder_name,
        "Established In": establishment_info_dict.get("Year estd.", ""),
        "Total Projects": establishment_info_dict.get("Projects", ""),
        "Icon": icon_link,
        "About Builder": builder_description,    
    }
    return builder_data


def parse_project_data(soup):
    project_data = {}

    # Last Updated At
    last_updated_at_text = soup.find("div", class_="css-1iv3lhr").find('div').text
    last_updated_at = last_updated_at_text.split(":")[-1].strip()

    # Basic Info
    project_name = soup.find("div", class_="css-js5v7e").find('h1').text
    project_by = soup.find("div", class_="css-1bcji2n").find('a').text
    builder_info_link = http_host + "://" + host_name + soup.find("a", class_="css-l2kny5").get("href")

    builder_data = parse_builder_details(builder_info_link)

    project_location = soup.find("div", class_="css-1ty5xzi").text


    # Prices
    price_range = soup.find("div", class_="css-1hidc9c").find('span', 'css-19rl1ms').text
    min_price = price_range.split("-")[0].strip()
    max_price = price_range.split("-")[-1].strip()
    per_sq_ft_price_text = soup.find("div", class_="css-1hidc9c").find('span', 'css-124qey8')
    per_sq_ft_price = per_sq_ft_price_text.text if per_sq_ft_price_text else ""

    project_data = {
        "Last updated": last_updated_at,
        "Project Name": project_name,
        "Min Price": min_price,
        "Max Price": max_price,
        "Per sq. ft. Price": u"".join(per_sq_ft_price),
        "By": project_by,
        "Location": project_location,
    }

    project_data.update(builder_data)
    return project_data

def parse_configurations(soup):
    project_configurations = soup.find("section", class_="css-13dph6").find_all("div", class_="css-c2zxhw")

    project_configurations_dict = {}
    for project_c in project_configurations:
        key = project_c.find("div", class_="css-0").text
        if key in ("Size", "Sizes"):
            value = [
                project_c.find("div", class_="css-1k19e3").text,
                project_c.find("div", class_="css-w788ou").text
            ]
        else:
            value = project_c.find("div", class_="css-1k19e3").text
        
        project_configurations_dict.update({key: value})

    size_val = project_configurations_dict.get("Sizes", [])
    if not size_val:
        size_val = project_configurations_dict.get("Size", [])


    min_size = size_val[0].split("-")[0].strip()
    max_size = size_val[0].split("-")[-1].strip()
    sizes_type = size_val[1].split("-")[-1].strip()
    


    return {
        "Configurations": project_configurations_dict.get("Configurations", ""),
        "Configuration": project_configurations_dict.get("Configuration", ""),
        "Possession Starts": project_configurations_dict.get("Possession Starts", ""),
        "Possession Status": project_configurations_dict.get("Possession Status", ""),
        "Avg. Price": u"".join(
            project_configurations_dict.get("Avg. Price", ""),
            ),
        "Min Sizes": min_size,
        "Max Sizes": max_size,
        "Sizes Type": sizes_type.replace("(", "").replace(")", ""),
    }

def parse_tab_section(soup):
    
    tab_project_info = soup.find("tbody", class_="css-1mkc5st").find_all("tr")
    
    project_info_dict = {}
    for info in tab_project_info:
        key = info.find("th").text
        value = info.find("td").text
        project_info_dict.update({
            key: value
        })
    
    return {
        "Tab Project Area": project_info_dict.get("Project Area", ""),
        "Tab Sizes": project_info_dict.get("Sizes", "") or project_info_dict.get("size", ""),
        "Tab Project Size": project_info_dict.get("Project Size", ""),
        "Tab Launch Date": project_info_dict.get("Launch Date", ""),
        "Tab Avg. Price": project_info_dict.get("Avg. Price", ""),
        "Tab Possession Status": project_info_dict.get("Possession Status", ""),
        "Tab Possession Starts": project_info_dict.get("Possession Starts", ""),
        "Tab Configurations": project_info_dict.get("Configurations", ""),
        "Tab Configuration": project_info_dict.get("Configuration", ""),
        "Tab Rera Id": project_info_dict.get("Rera Id", ""),
    }

def parse_project_description(soup):
    project_description_obj = soup.find("div", class_="css-11besvp")
    project_description = project_description_obj.text if project_description_obj else project_description_obj
    return {"About Project": project_description}

def parse_project_amenities(soup):
    project_amenities = []
    
    amenity_obj_list = soup.find("section", attrs={"id": "amenities"}).find("div", class_="css-a9s06j").find("section").find("div")

    for amenity_obj in amenity_obj_list:
        amenity_text = amenity_obj.text 
        if 'Less' not in amenity_text:
            project_amenities.append(amenity_text)

    return {"Amenities": project_amenities}



def find_project_details(url):
    response = send_get_request(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    project_data = {
        "Project Page Link": url,
    }
    
    project_data.update(parse_project_data(soup))
    project_data.update(parse_configurations(soup))
    project_data.update(parse_tab_section(soup))
    project_data.update(parse_project_description(soup))
    project_data.update(parse_project_amenities(soup))
    
    return project_data


def iterate_project_listings(soup):
    # Loop through each project listing and extract data
    project_info_list = []
    article_num = 0

    # Find `all the project listings on the page
    project_listing = soup.find("div", class_="css-0")
        
    if not project_listing:
        print("Oops! Failed to scrape project listings.")
        return []

    project_list = project_listing.findChildren("div" , recursive=False)
    for ix, project in enumerate(project_list):
        project_info_section = project.find("div", class_="css-zrd0bv")
        project_url_div = project.find("a", class_="_j31fk8 _c8uea4 _g3exct _csbfng _frwh2y _ks15vq _vv1q9c _sq1l2s")
        if project_url_div:
            project_page_url = http_host + "://" + host_name + project_url_div.get("href")
            print(f"Project {ix}: project_page_url -> {project_page_url}")
            project_info = find_project_details(project_page_url)
            project_info_list.append(project_info)
            # break
        # else:
            # print(f"Project {ix}: is failed to load resources or requested page is not relevant to project description")
        
    return project_info_list



def parse_project_info(project_info_list):
    return  [
        OrderedDict({
        "Last updated": p.get("Last updated", ""),
        "Project Name": p.get("Project Name", ""),
        "Min Price": p.get("Min Price", ""),
        "Max Price": p.get("Max Price", ""),
        "Per sq. ft. Prrice": p.get("Per sq. ft. Prrice", ""),
        "By": p.get("By", ""),
        "Location": p.get("Location", ""),
        "Configurations": p.get("Configurations", ""),
        "Configuration": p.get("Configuration", ""),
        "Possession Starts": p.get("Possession Starts", ""),
        "Possession Status": p.get("Possession Status", ""),
        "Avg. Price": p.get("Avg. Price", ""),
        "Min Sizes": p.get("Min Sizes", ""),
        "Max Sizes": p.get("Max Sizes", ""),
        "Sizes Type": p.get("Sizes Type", ""),
        "Tab Project Area": p.get("Tab Project Area", ""),
        "Tab Sizes": p.get("Tab Sizes", ""),
        "Tab Project Size": p.get("Tab Project Size", ""),
        "Tab Launch Date": p.get("Tab Launch Date", ""),
        "Tab Avg. Price": p.get("Tab Avg. Price", ""),
        "Tab Possession Status": p.get("Tab Possession Status", ""),
        "Tab Possession Starts": p.get("Tab Possession Starts", ""),
        "Tab Configurations": p.get("Tab Configurations", ""),
        "Tab Configuration": p.get("Tab Configuration", ""),
        "Tab Rera Id": p.get("Tab Rera Id", ""),
        "About Project": p.get("About Project", ""),
        "You tube Link": p.get("You tube Link", ""),
        "Amenities": p.get("Amenities", ""),
        "Neighbourhood": p.get("Neighbourhood", ""),
        "Builder Name": p.get("Builder Name", ""),
        "Established In": p.get("Established In", ""),
        "Total Projects": p.get("Total Projects", ""),
        "Icon": p.get("Icon", ""),
        "About Builder": p.get("About Builder", ""),
        "Project Page Link": p.get("Project Page Link", ""),
    })
    for p
    in project_info_list
    ]

def save_excel_file(file_name, parsed_project_info_list):
    df = pd.DataFrame.from_records(parsed_project_info_list)
    df.to_excel(file_name, index=False)


# %%
# URL of the webpage
url = "https://housing.com/in/buy/searches/AE0P38f9yfbk7p3m2h1f"


# website info
url_split = url.split("://")
http_host = url_split[0]
host_name = url_split[-1].split("/", 1)[0]

def main():
    # Send an HTTP GET request to the URL
    response = requests.get(url)


    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # list projects one by one
    project_info_list = iterate_project_listings(soup)

    # parsing project_info_list
    parsed_project_info_list = parse_project_info(project_info_list)

    # saviing into file
    file_name = "./project_data.xlsx"
    save_excel_file(file_name, parsed_project_info_list)

    # Save the data to an Excel file
    print(f"Successfully scraped the given url -> {url} and data us and saved to {file_name}")
    
main()
