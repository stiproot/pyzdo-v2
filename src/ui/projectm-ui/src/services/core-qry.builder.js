export const buildCoreQry = (collection, id, projectId) => {
  const qry = {
    qry_data: {
      // ql:
      //   `select * from ` +
      //   `pyzdo.${scope}.${collection} ` +
      //   `where id = '${id}' and __metadata__.project_id = '${projectId}'`,
      ql:
        `SELECT * FROM c ` +
        `WHERE c.id = '${id}' AND c.__metadata__.project_id = '${projectId}'`,
      params: [],
      collection_name: collection,
    },
    filter: {
      node_type: collection,
    },
  };

  return qry;
};
