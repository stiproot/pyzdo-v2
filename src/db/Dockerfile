FROM couchbase:latest

# VOLUME /opt/couchbase/var/lib/couchbase
# VOLUME_IF_NECESSARY /opt/couchbase/var/lib/couchbase/index

COPY init-init-cluster.sh /opt/couchbase/init-init-cluster.sh
COPY init-create-bucket.sh /opt/couchbase/init-create-bucket.sh
COPY init-create-scope.sh /opt/couchbase/init-create-scope.sh
COPY init-create-collection.sh /opt/couchbase/init-create-collection.sh
COPY init.sh /opt/couchbase/init.sh
COPY indx.sh /opt/couchbase/indx.sh

RUN chmod +x /opt/couchbase/init-init-cluster.sh
RUN chmod +x /opt/couchbase/init-create-bucket.sh
RUN chmod +x /opt/couchbase/init-create-scope.sh
RUN chmod +x /opt/couchbase/init-create-collection.sh
RUN chmod +x /opt/couchbase/init.sh
RUN chmod +x /opt/couchbase/indx.sh

CMD ["./opt/couchbase/init.sh"]
