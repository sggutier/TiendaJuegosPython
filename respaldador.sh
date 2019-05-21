#!/bin/bash
mysqldump -u root --password='' ventas > ventas$(/bin/date "+%Y%m%d-%H%M").sql
