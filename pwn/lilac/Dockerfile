FROM ubuntu:20.04

RUN apt-get update && apt-get install -y xinetd && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*
RUN useradd -U -m lilac && mkdir -p /home/lilac
RUN chown -R root:lilac /home/lilac && chmod 750 /home/lilac

CMD /home/lilac/startchall
