#!/bin/bash

pushd /var/log/pagerduty-icinga2-webhook

if [ -f "webhooks_result.txt" ]; then
  mv webhooks_result.txt webhooks_result.txt.old
fi

curl -s https://app.pagerduty.com/webhook_ips | jq '.'[] | sort | sed 's/"//g' | sed 's/$/;/g' > webhooks_result.txt

if [ -f "webhooks_result.txt.old" ]; then
  DIFF=$(diff -q 'webhooks_result.txt.old' 'webhooks_result.txt' > /dev/null)
  if [ $? -ne 0 ]; then
    mail -s "PagerDuty webhook IP change detected" your@email < webhooks_result.txt
  fi
  rm webhooks_result.txt.old
fi

popd
