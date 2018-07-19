from setuptools import setup, find_packages

setup(
    name="Pagerduty-Icinga2-Webhook",
    version=1.0,
    description="Listens for PagerDuty webhooks and acknowledges Icinga2 service.",
    url="https://github.com/eric-price/pagerduty-icinga2-webhook",
    author='Eric Price',
    author_email='eric2025@gmail.com',
    packages=find_packages(),
    install_requires=[
        'gunicorn>=19.7.1',
        'flask>=0.12.2',
        'python-icinga2api>=0.3',
        'requests>=2.18.4',
    ],
)
