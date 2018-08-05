# Generated by Django 2.1 on 2018-08-05 16:21

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_admin', models.BooleanField(default=False, verbose_name='صلاحية المدير')),
                ('location', models.CharField(max_length=50, verbose_name='العنوان')),
                ('phone_number', models.CharField(max_length=8, unique=True, validators=[django.core.validators.RegexValidator(message='يجب أن تحتوي أرقام الهاتف على 8 أرقام.', regex='^\\d{8}$')], verbose_name='الهاتف')),
                ('city', models.CharField(max_length=25, verbose_name='المدينة')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'مستخدم',
                'verbose_name_plural': 'المستخدمين',
                'ordering': ['created_at'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sid', models.CharField(max_length=255, unique=True)),
                ('sender', models.CharField(default='', max_length=255)),
                ('recipient', models.CharField(default='', max_length=255)),
                ('body', models.TextField(blank=True, default='')),
                ('price', models.TextField(blank=True, default='')),
                ('is_outbound', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الأنشاء')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')),
                ('money', models.CharField(blank=True, max_length=255, verbose_name='المبلغ')),
                ('fee', models.CharField(blank=True, max_length=255, verbose_name='الرسوم')),
                ('beneficiary_number', models.CharField(max_length=8, validators=[django.core.validators.RegexValidator(message='يجب أن تحتوي أرقام الهاتف على 8 أرقام.', regex='^\\d{8}$')], verbose_name='رقم المستفيد')),
                ('is_done', models.BooleanField(default=True, verbose_name='تم الإيتلام')),
                ('inbound_sid', models.CharField(default='', max_length=255)),
                ('agent_outbound_sid', models.CharField(max_length=255, unique=True)),
                ('beneficiary_outbound_sid', models.CharField(max_length=255, unique=True)),
                ('from_agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='committed', to=settings.AUTH_USER_MODEL, verbose_name='العميل المرسل')),
                ('to_agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received', to=settings.AUTH_USER_MODEL, verbose_name='العميل المستلم')),
            ],
            options={
                'verbose_name': 'تحويلة',
                'verbose_name_plural': 'التحويلات',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='InboundMessage',
            fields=[
                ('message_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.Message')),
            ],
            options={
                'verbose_name': 'رسالة واردة',
                'verbose_name_plural': 'الرسائل الواردة',
                'ordering': ['created_at'],
            },
            bases=('main.message',),
        ),
        migrations.CreateModel(
            name='OutboundMessage',
            fields=[
                ('message_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.Message')),
                ('status', models.CharField(choices=[('accepted', 'Accepted'), ('queued', 'Queued'), ('sending', 'Sending'), ('sent', 'Sent'), ('receiving', 'Receiving'), ('received', 'Received'), ('delivered', 'Delivered'), ('undelivered', 'Undelivered'), ('failed', 'Failed')], default='accepted', max_length=25)),
            ],
            options={
                'verbose_name': 'رسالة صادرة',
                'verbose_name_plural': 'الرسائل الصادرة',
                'ordering': ['created_at'],
            },
            bases=('main.message',),
        ),
    ]
