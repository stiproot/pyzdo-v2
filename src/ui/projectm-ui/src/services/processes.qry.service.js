import { qry } from "./qry.http.service.js";
import { buildCoreQry } from "./core-qry.builder.js";
import { COLLECTIONS } from "@/services/store.enum.js";

export async function getProcess(id, projectId) {
  try {
    const req = buildCoreQry(
      COLLECTIONS.PROCESS_DEFINITIONS,
      id,
      projectId
    );
    const data = await qry(req);
    return data[0];
  } catch (error) {
    console.error("GET request error:", error);
    return [];
  }
}

export async function getProcesses(ids) {
  try {
    const formattedIds = ids.map((id) => `'${id}'`).join(",");

    // const ql =
    //   `select * from ` +
    //   `${BUCKET}.${SCOPES.DEFINITIONS}.${COLLECTIONS.PROCESS_DEFINITIONS} ` +
    //   `where id in [${formattedIds}]`;
    const ql =
      `SELECT * FROM c ` +
      `WHERE c.id IN (${formattedIds})`;

    const req = {
      qry_data: {
        ql: ql,
        params: [],
        collection_name: COLLECTIONS.PROCESS_DEFINITIONS,
      },
      filter: {
        node_type: COLLECTIONS.PROCESS_DEFINITIONS,
      },
    };

    const data = await qry(req);
    return data;
  } catch (error) {
    console.error("GET request error:", error);
    return [];
  }
}
