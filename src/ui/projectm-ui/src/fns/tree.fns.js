export const enrichTree = (data) => {
  const enriched = data.map((node) => {
    const enrichedNode = {
      ...node,
      label: `${node.id} - ${node.type} - ${node.title}`,
      children: node.children ? enrichTree(node.children) : [],
    };

    return enrichedNode;
  });

  return enriched;
};

export const getTasks = (node, tasks) => {
  if (node.children && node.children.length) {
    node.children.forEach((child) => {
      getTasks(child, tasks);
    });
  }

  if (node.type === "Task") {
    tasks.push(node);
  }
};

export const filterTree = (tree, predicates) => {
  return coreFilterTree(tree, predicates);
};

export const coreFilterTree = (tree, predicates) => {
  const filteredChildren = filterChildren(tree.children, predicates);
  const filteredTree = {
    ...tree,
    children: filteredChildren,
  };
  return filteredTree;
};

export const filterChildren = (data, predicates) => {
  if (!data) {
    return [];
  }

  const filteredData = filterNode(data, predicates);

  const enriched = filteredData.map((node) => {
    const enrichedNode = {
      ...node,
      children: node.children ? filterChildren(node.children, predicates) : [],
    };

    return enrichedNode;
  });

  return enriched;
};

export const filterNode = (data, predicates) => {
  const filtered = data.filter((node) => {
    if (node.type === "Task") {
      if (predicates && predicates.length) {
        let accum = true;

        for (const i in predicates) {
          if (predicates[i]) accum = accum && predicates[i](node);
        }

        return accum;
      }

      return true;
    }

    return true;
  });

  return filtered;
};

export const orAccumFilter = (data, predicates) => {
  const filtered = data.filter((node) => {
    if (node.type === "Task") {
      let accum = false;
      for (const i in predicates) {
        accum = accum || predicates[i](node);
      }
      return accum;
    }
    return true;
  });

  return filtered;
};

export const andAccumFilter = (data, predicates) => {
  const filtered = data.filter((node) => {
    if (node.type === "Task") {
      let accum = true;
      for (const i in predicates) {
        accum = accum && predicates[i](node);
      }
      return accum;
    }
    return true;
  });

  return filtered;
};
