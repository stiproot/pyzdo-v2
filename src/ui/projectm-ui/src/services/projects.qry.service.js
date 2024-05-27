import { qry } from "./qry.http.service.js";
import { COLLECTIONS } from "@/services/store.enum.js";

export async function getProject(id) {
  try {
    const req = {
      qry_data: {
        ql:
          `SELECT * ` +
          `FROM c ` +
          `WHERE c.id = '${id}'`,
        params: [],
        collection_name: COLLECTIONS.PROJECT_DEFINITIONS,
      },
      filter: {
        node_type: COLLECTIONS.PROJECT_DEFINITIONS,
      },
    };

    const data = await qry(req);
    return data[0];
  } catch (error) {
    console.error("GET request error:", error);
    return [];
  }
}

export async function getProjects() {
  try {
    const req = {
      qry_data: {
        ql: `SELECT * FROM c`,
        params: [],
        collection_name: COLLECTIONS.PROJECT_DEFINITIONS,
      },
      filter: {
        node_type: COLLECTIONS.PROJECT_DEFINITIONS,
      },
    };

    const data = await qry(req);
    return data.slice().sort((a, b) => a.id.localeCompare(b.id));
  } catch (error) {
    console.error("GET request error:", error);
    return [];
  }
}
