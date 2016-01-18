# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class AllProjectInfo(models.Model):
    project_no = models.IntegerField(db_column='Project_No')  # Field name made lowercase.
    developer_id = models.IntegerField(db_column='Developer_id')  # Field name made lowercase.
    developer_acc_no = models.IntegerField(db_column='Developer_Acc_No')  # Field name made lowercase.
    developer_name = models.CharField(db_column='Developer_Name', max_length=255)  # Field name made lowercase.
    project_name = models.CharField(db_column='Project_Name', max_length=50)  # Field name made lowercase.
    developer_acc_name = models.CharField(db_column='Developer_Acc_Name', max_length=255)  # Field name made lowercase.
    project_logo_file = models.CharField(db_column='Project_logo_File', max_length=255)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=255)  # Field name made lowercase.
    road = models.IntegerField(db_column='Road')  # Field name made lowercase.
    road_name = models.CharField(db_column='Road_Name', max_length=255)  # Field name made lowercase.
    project_city = models.IntegerField(db_column='Project_City')  # Field name made lowercase.
    project_city_name = models.CharField(db_column='Project_City_Name', max_length=50)  # Field name made lowercase.
    project_suburb = models.IntegerField(db_column='Project_Suburb')  # Field name made lowercase.
    project_suburb_name = models.CharField(db_column='Project_Suburb_Name', max_length=50)  # Field name made lowercase.
    project_area = models.IntegerField(db_column='Project_Area')  # Field name made lowercase.
    project_area_name = models.CharField(db_column='Project_Area_Name', max_length=50)  # Field name made lowercase.
    project_location = models.IntegerField(db_column='Project_Location')  # Field name made lowercase.
    project_location_name = models.CharField(db_column='Project_Location_Name', max_length=50)  # Field name made lowercase.
    pincode = models.CharField(db_column='Pincode', max_length=10)  # Field name made lowercase.
    project_status = models.CharField(db_column='Project_Status', max_length=50)  # Field name made lowercase.
    project_possession = models.DateField(db_column='Project_Possession')  # Field name made lowercase.
    listing_factor = models.DecimalField(db_column='Listing_Factor', max_digits=10, decimal_places=4)  # Field name made lowercase.
    realty_banner_flag = models.CharField(max_length=10)
    project_subscription = models.IntegerField(db_column='Project_Subscription')  # Field name made lowercase.
    display_price = models.CharField(db_column='Display_Price', max_length=3)  # Field name made lowercase.
    display_area = models.CharField(db_column='Display_Area', max_length=3)  # Field name made lowercase.
    display_possession = models.CharField(db_column='Display_Possession', max_length=5, blank=True, null=True)  # Field name made lowercase.
    display_under_construction = models.CharField(db_column='Display_Under_Construction', max_length=3)  # Field name made lowercase.
    map_latitude = models.FloatField(db_column='Map_Latitude')  # Field name made lowercase.
    hdfc_banner_flag = models.CharField(max_length=10)
    display_possession_month = models.CharField(max_length=3)
    hdfc_approved = models.CharField(db_column='HDFC_Approved', max_length=50)  # Field name made lowercase.
    sub_type = models.CharField(db_column='Sub_Type', max_length=50)  # Field name made lowercase.
    booking_start_dt = models.DateField(db_column='Booking_Start_Dt')  # Field name made lowercase.
    possession = models.DateField(db_column='Possession')  # Field name made lowercase.
    possession_text = models.CharField(db_column='Possession_Text', max_length=50, blank=True, null=True)  # Field name made lowercase.
    display_instahomeloan = models.CharField(max_length=3)
    neighbour_status = models.CharField(db_column='Neighbour_Status', max_length=3)  # Field name made lowercase.
    map_longitude = models.FloatField(db_column='Map_Longitude')  # Field name made lowercase.
    project_config_no = models.IntegerField(db_column='Project_Config_No')  # Field name made lowercase.
    config_type = models.CharField(db_column='Config_Type', max_length=50)  # Field name made lowercase.
    carpet_area = models.IntegerField(db_column='Carpet_Area')  # Field name made lowercase.
    built_up_area = models.IntegerField(db_column='Built_Up_Area')  # Field name made lowercase.
    no_of_balconies = models.IntegerField(db_column='No_Of_Balconies')  # Field name made lowercase.
    configuration_name = models.CharField(db_column='Configuration_Name', max_length=50)  # Field name made lowercase.
    config_feature = models.CharField(max_length=50, blank=True, null=True)
    no_of_floors = models.IntegerField(db_column='No_Of_floors')  # Field name made lowercase.
    no_of_bedroom = models.CharField(db_column='No_Of_Bedroom', max_length=50)  # Field name made lowercase.
    no_of_bathroom = models.IntegerField(db_column='No_Of_Bathroom')  # Field name made lowercase.
    no_of_units_available = models.IntegerField(db_column='No_Of_Units_available')  # Field name made lowercase.
    floor_rise = models.IntegerField(db_column='Floor_Rise')  # Field name made lowercase.
    super_open_area = models.IntegerField(db_column='Super_open_area')  # Field name made lowercase.
    minimum_price = models.IntegerField(db_column='Minimum_Price')  # Field name made lowercase.
    maximum_price = models.IntegerField(db_column='Maximum_Price')  # Field name made lowercase.
    monthly_maintenance = models.FloatField(db_column='Monthly_Maintenance')  # Field name made lowercase.
    area_type = models.CharField(db_column='Area_Type', max_length=50)  # Field name made lowercase.
    area_value = models.CharField(db_column='Area_Value', max_length=15)  # Field name made lowercase.
    area_unit = models.CharField(db_column='Area_Unit', max_length=50)  # Field name made lowercase.
    base_price = models.IntegerField(db_column='Base_Price')  # Field name made lowercase.
    status_dt = models.DateField(db_column='Status_Dt')  # Field name made lowercase.
    project_image_file = models.CharField(db_column='Project_Image_File', max_length=500)  # Field name made lowercase.
    map_config = models.CharField(max_length=50)
    area_value_sort = models.FloatField(db_column='Area_Value_Sort')  # Field name made lowercase.
    video_walkthrough = models.CharField(db_column='Video_Walkthrough', max_length=255, blank=True, null=True)  # Field name made lowercase.
    project_views = models.IntegerField(db_column='Project_Views', blank=True, null=True)  # Field name made lowercase.
    store_views = models.IntegerField(db_column='Store_Views', blank=True, null=True)  # Field name made lowercase.
    hasstore = models.CharField(db_column='HasStore', max_length=10, blank=True, null=True)  # Field name made lowercase.
    possesiontext = models.CharField(db_column='PossesionText', max_length=10)  # Field name made lowercase.
    gallery_count = models.IntegerField(db_column='Gallery_Count')  # Field name made lowercase.
    hasdeal = models.CharField(db_column='HasDeal', max_length=10)  # Field name made lowercase.
    p_minprice = models.IntegerField(db_column='P_MinPrice')  # Field name made lowercase.
    p_maxprice = models.IntegerField(db_column='P_MaxPrice')  # Field name made lowercase.
    p_config_string = models.CharField(db_column='P_Config_String', max_length=50)  # Field name made lowercase.
    img_project_plan = models.CharField(db_column='Img_Project_Plan', max_length=2)  # Field name made lowercase.
    img_site_plan = models.CharField(db_column='Img_Site_Plan', max_length=2)  # Field name made lowercase.
    img_floor_plan = models.CharField(db_column='Img_Floor_Plan', max_length=2)  # Field name made lowercase.
    img_config_plan = models.CharField(db_column='Img_Config_Plan', max_length=2)  # Field name made lowercase.
    img_uc = models.CharField(db_column='Img_UC', max_length=2)  # Field name made lowercase.
    img_sample_flat = models.CharField(db_column='Img_Sample_Flat', max_length=2)  # Field name made lowercase.
    developer_logo_file = models.CharField(db_column='Developer_Logo_File', max_length=100)  # Field name made lowercase.
    price_change = models.CharField(db_column='Price_Change', max_length=50)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=15)  # Field name made lowercase.
    broker_developer_name = models.CharField(db_column='Broker_Developer_Name', max_length=60)  # Field name made lowercase.
    broker_developer_logo_file = models.CharField(db_column='Broker_Developer_Logo_File', max_length=100)  # Field name made lowercase.
    brochure_filename = models.CharField(db_column='Brochure_Filename', max_length=100)  # Field name made lowercase.
    emi = models.IntegerField(blank=True, null=True)
    srno = models.IntegerField(db_column='SrNo', blank=True, null=True)  # Field name made lowercase.
    priceperunit = models.CharField(db_column='PricePerUnit', max_length=45, blank=True, null=True)  # Field name made lowercase.
    project_description = models.CharField(max_length=500)
    project_remarks = models.TextField(db_column='Project_Remarks', blank=True, null=True)  # Field name made lowercase.
    amenity_code = models.CharField(max_length=250, blank=True, null=True)
    amenities = models.CharField(max_length=1000, blank=True, null=True)
    nearest_station_distance = models.IntegerField(blank=True, null=True)
    developer_overview = models.TextField(db_column='Developer_Overview', blank=True, null=True)  # Field name made lowercase.
    ppu_metric = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'all_project_info'

