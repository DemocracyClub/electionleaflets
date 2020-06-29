# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.


from django.db import models


class legacyAuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = "auth_group"


class legacyAuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "auth_group_permissions"


class AuthMessage(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user_id = models.IntegerField()
    message = models.TextField()

    class Meta:
        managed = False
        db_table = "auth_message"


class legacyAuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=50)
    content_type_id = models.IntegerField()
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "auth_permission"


class legacyAuthUser(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    password = models.CharField(max_length=128)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    is_superuser = models.IntegerField()
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "auth_user"


class legacyAuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user_id = models.IntegerField()
    group_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "auth_user_groups"


class legacyAuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "auth_user_user_permissions"


class legacyBoundariesBoundary(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    constituency_id = models.IntegerField()
    boundary = models.TextField()
    zoom = models.IntegerField()
    north = models.FloatField()
    south = models.FloatField()
    east = models.FloatField()
    west = models.FloatField()

    class Meta:
        managed = False
        db_table = "boundaries_boundary"


class legacyCategory(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    default_value = models.IntegerField(blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = "category"


class legacyConstituency(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=255)
    alternative_name = models.CharField(max_length=255, blank=True)
    constituency_type_id = models.IntegerField()
    retired = models.IntegerField(blank=True, null=True)
    area_code = models.CharField(max_length=20, blank=True)
    area_uri = models.CharField(max_length=255, blank=True)
    wikipedia_url = models.CharField(max_length=255, blank=True)
    url_id = models.CharField(max_length=100, blank=True)
    guardian_aristotle_id = models.IntegerField(blank=True, null=True)
    guardian_pa_code = models.IntegerField(blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True)
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "constituency"


class legacyConstituencySeq(models.Model):
    sequence = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "constituency_seq"


class legacyConstituencyType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=50)
    country_id = models.IntegerField()
    url_id = models.CharField(max_length=100, blank=True)

    class Meta:
        managed = False
        db_table = "constituency_type"


class legacyContentblock(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=64)
    content = models.TextField()

    class Meta:
        managed = False
        db_table = "contentblock"


class legacyCountry(models.Model):
    country_id = models.IntegerField(primary_key=True)
    iso = models.CharField(max_length=2)
    name = models.CharField(max_length=80)
    iso3 = models.CharField(max_length=3, blank=True)

    class Meta:
        managed = False
        db_table = "country"


class legacyDjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    action_time = models.DateTimeField()
    user_id = models.IntegerField()
    content_type_id = models.IntegerField(blank=True, null=True)
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.IntegerField()
    change_message = models.TextField()

    class Meta:
        managed = False
        db_table = "django_admin_log"


class legacyDjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "django_content_type"


class legacyDjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "django_session"


class legacyDjangoSite(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    domain = models.CharField(max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = "django_site"


class legacyEmailAlert(models.Model):
    email_alert_id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=50)
    frequency_hours = models.IntegerField()
    last_sent = models.DateTimeField(blank=True, null=True)
    type = models.CharField(max_length=50)
    parent_id = models.IntegerField()
    activated = models.IntegerField(blank=True, null=True)
    confirm_id = models.CharField(max_length=100)
    title = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "email_alert"


class legacyEmailAlertSeq(models.Model):
    sequence = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "email_alert_seq"


class legacyEmailQue(models.Model):
    email_que_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=765)
    email = models.CharField(max_length=765)
    postcode = models.CharField(max_length=60)
    delivery_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "email_que"


class legacyImageQue(models.Model):
    image_que_id = models.IntegerField(primary_key=True)
    upload_key = models.CharField(max_length=255)
    name = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)
    image_key = models.CharField(max_length=255, blank=True)
    uploaded_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "image_que"


class legacyImageQueSeq(models.Model):
    sequence = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "image_que_seq"


class legacyLeaflet(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    publisher_party = models.ForeignKey("legacyParty")
    postcode = models.CharField(max_length=50, blank=True)
    lng = models.FloatField()
    lat = models.FloatField()
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    date_uploaded = models.DateTimeField()
    date_delivered = models.DateTimeField()
    live = models.IntegerField(blank=True, null=True)
    imprint = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = "leaflet"


class legacyLeafletCategory(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    leaflet_id = models.IntegerField()
    category_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "leaflet_category"


class legacyLeafletCategorySeq(models.Model):
    sequence = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "leaflet_category_seq"


class legacyLeafletConstituency(models.Model):
    leaflet = models.ForeignKey("legacyLeaflet")
    constituency = models.ForeignKey("legacyConstituency")

    class Meta:
        managed = False
        db_table = "leaflet_constituency"


class legacyLeafletConstituencySeq(models.Model):
    sequence = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "leaflet_constituency_seq"


class legacyLeafletElectionSeq(models.Model):
    sequence = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "leaflet_election__seq"


class legacyLeafletImage(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    leaflet = models.ForeignKey(
        legacyLeaflet, related_name="images", on_delete=models.CASCADE
    )
    image_key = models.CharField(max_length=255)
    sequence = models.IntegerField()

    class Meta:
        managed = False
        db_table = "leaflet_image"


class legacyLeafletImageSeq(models.Model):
    sequence = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "leaflet_image_seq"


class legacyLeafletPartyAttack(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    leaflet_id = models.IntegerField()
    party_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "leaflet_party_attack"


class legacyLeafletPartyAttackSeq(models.Model):
    sequence = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "leaflet_party_attack_seq"


class legacyLeafletSeq(models.Model):
    sequence = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "leaflet_seq"


class legacyLeafletTag(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    leaflet_id = models.IntegerField()
    tag_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "leaflet_tag"


class legacyLeafletTagSeq(models.Model):
    sequence = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "leaflet_tag_seq"


class legacyLeafletsUploadsession(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    key = models.CharField(max_length=64, blank=True)
    image1 = models.CharField(max_length=255, blank=True)
    image2 = models.CharField(max_length=255, blank=True)
    image3 = models.CharField(max_length=255, blank=True)
    image4 = models.CharField(max_length=255, blank=True)
    image5 = models.CharField(max_length=255, blank=True)
    image6 = models.CharField(max_length=255, blank=True)
    image7 = models.CharField(max_length=255, blank=True)
    image8 = models.CharField(max_length=255, blank=True)
    s3keys = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = "leaflets_uploadsession"


class legacyParty(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=255)
    country_id = models.IntegerField()
    major = models.IntegerField(blank=True, null=True)
    logo_file = models.CharField(max_length=100, blank=True)
    url_id = models.CharField(max_length=255, blank=True)
    colour = models.CharField(max_length=6, blank=True)
    twitter_account = models.CharField(max_length=50, blank=True)
    force_top = models.IntegerField(blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True)
    popular = models.IntegerField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    show_on_add_page = models.IntegerField()

    class Meta:
        managed = False
        db_table = "party"


class legacyPromise(models.Model):
    promise_id = models.IntegerField(primary_key=True)
    leaflet_id = models.IntegerField()
    detail = models.TextField()

    class Meta:
        managed = False
        db_table = "promise"


class legacyRateInteresting(models.Model):
    rate_interesting_id = models.IntegerField(primary_key=True)
    leaflet_id = models.IntegerField()
    description = models.TextField()
    user_name = models.CharField(max_length=255)
    user_email = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "rate_interesting"


class legacyRateInterestingSeq(models.Model):
    sequence = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "rate_interesting_seq"


class legacyRateType(models.Model):
    rate_type_id = models.IntegerField(primary_key=True)
    left_label = models.CharField(max_length=50)
    right_label = models.CharField(max_length=50, blank=True)

    class Meta:
        managed = False
        db_table = "rate_type"


class legacyRateValue(models.Model):
    rate_value_id = models.IntegerField(primary_key=True)
    leaflet_id = models.IntegerField()
    user_name = models.CharField(max_length=100)
    user_email = models.CharField(max_length=100)
    rate_type_id = models.IntegerField()
    value = models.IntegerField()

    class Meta:
        managed = False
        db_table = "rate_value"


class legacyRateValueSeq(models.Model):
    sequence = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "rate_value_seq"


class SouthMigrationhistory(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app_name = models.CharField(max_length=255)
    migration = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "south_migrationhistory"


class legacyTag(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    tag = models.CharField(max_length=255)
    tag_clean = models.CharField(max_length=255, blank=True)
    dead = models.IntegerField(blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = "tag"


class legacyTagSeq(models.Model):
    sequence = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "tag_seq"
