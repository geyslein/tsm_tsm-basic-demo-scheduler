FROM git.ufz.de:4567/rdm-software/timeseries-management/tsm-extractor/extractor:latest as base

FROM base as build

USER root

RUN apt-get -y update \
    && apt-get -y install \
      python3-pip \
      curl \
      unzip

# add requirements
COPY src/requirements.txt /tmp/requirements.txt
RUN pip install \
        --no-cache-dir \
        --no-warn-script-location -r \
        /tmp/requirements.txt

FROM base as dist

# Create a group and user
# Already there in base image
# RUN useradd --uid 1000 -m appuser

# Add python packages
COPY --from=build /usr/local/lib/python3.9/dist-packages /usr/local/lib/python3.9/dist-packages

# Tell docker that all future commands should run as the appuser user
USER appuser

WORKDIR /home/appuser/app/basic_demo_scheduler

COPY src .

ENTRYPOINT ["python3", "main.py"]