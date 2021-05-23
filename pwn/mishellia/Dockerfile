FROM ubuntu:20.04

RUN apt-get update && apt-get install -y xinetd && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*
RUN useradd -U -m mishellia && mkdir -p /home/mishellia
RUN chown -R root:mishellia /home/mishellia && chmod 750 /home/mishellia

CMD /home/mishellia/startchall
