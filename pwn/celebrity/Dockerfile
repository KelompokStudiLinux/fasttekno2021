FROM ubuntu:20.04

RUN apt-get update && apt-get install -y xinetd && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*
RUN useradd -U -m celebrity && mkdir -p /home/celebrity
RUN chown -R root:celebrity /home/celebrity && chmod 750 /home/celebrity

CMD /home/celebrity/startchall
