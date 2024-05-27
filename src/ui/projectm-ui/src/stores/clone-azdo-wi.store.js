import { defineStore } from "pinia";
import { computed } from "vue";
import { ext } from "@/services/azdo-proxy.service";
import { CMD_TYPES } from "@/services/cmd-types.enum.js";
import { generateGuid } from "@/services/guids.service";

const defaultState = () => ({
  id: null,
  parentId: null,
  iterationPath: null,
  areaPath: null,
  tags: null,
});

const ACTIONS = {
  INIT: "init",
  UPSERT: "upsert",
  SET_ID: "setId",
  SET_PARENT_ID: "setParentId",
  SET_ITERATION_PATH: "setIterationPath",
  SET_AREA_PATH: "setAreaPath",
  SET_TAGS: "setTags",
};

const GETTERS = {
  IS_VALID_STATE: "isValidState",
  GET_STATE: "getState",
  GET_ID: "getId",
  GET_PARENT_ID: "getParentId",
  GET_ITERATION_PATH: "getIterationPath",
  GET_AREA_PATH: "getAreaPath",
  GET_TAGS: "getTags",
};

const actions = {
  [ACTIONS.INIT](data) {
    const { id, parentId, iterationPath, areaPath, tags } =
      data || defaultState();

    this[ACTIONS.SET_ID](id);
    this[ACTIONS.SET_PARENT_ID](parentId);
    this[ACTIONS.SET_ITERATION_PATH](iterationPath);
    this[ACTIONS.SET_AREA_PATH](areaPath);
    this[ACTIONS.SET_TAGS](tags);
  },
  async [ACTIONS.UPSERT](idempotencyId) {
    const cmd = {
      idempotencyId: idempotencyId || generateGuid(),
      projectId: "default",
      cmdType: CMD_TYPES.CLONE_UNIT_OF_WORK,
      cmdData: { cmd: this.$state },
    };
    await ext(cmd);
  },

  [ACTIONS.SET_ID](value) {
    this.id = value;
  },
  [ACTIONS.SET_PARENT_ID](value) {
    this.parentId = value;
  },
  [ACTIONS.SET_ITERATION_PATH](value) {
    this.iterationPath = value;
  },
  [ACTIONS.SET_AREA_PATH](value) {
    this.areaPath = value;
  },
  [ACTIONS.SET_TAGS](value) {
    this.tags = value;
  },
};

const getters = {
  [GETTERS.IS_VALID_STATE]() {
    return (
      this.id &&
      this.parentId &&
      this.iterationPath &&
      this.areaPath &&
      this.tags
    );
  },
  [GETTERS.GET_STATE]() {
    return this.$state;
  },
  [GETTERS.GET_ID]() {
    return this.id;
  },
  [GETTERS.GET_PARENT_ID]() {
    return this.parentId;
  },
  [GETTERS.GET_ITERATION_PATH]() {
    return this.iterationPath;
  },
  [GETTERS.GET_AREA_PATH]() {
    return this.areaPath;
  },
  [GETTERS.GET_TAGS]() {
    return this.tags;
  },
};

export const useCloneAzdoWiStore = defineStore("clone-azdo-wi-store", {
  state: () => defaultState(),
  actions: { ...actions },
  getters: { ...getters },
});

export class CloneAzdoWiProvider {
  constructor(store) {
    this._store = store;
    this.init = this.init.bind(this);
    this.upsert = this.upsert.bind(this);
  }

  async init(data) {
    await this._store[ACTIONS.INIT](data);
  }

  async upsert(idempotencyId) {
    await this._store[ACTIONS.UPSERT](idempotencyId);
  }

  get isValidState() {
    return computed(() => this._store[GETTERS.IS_VALID_STATE]);
  }

  get state() {
    return computed(() => this._store[GETTERS.GET_STATE]);
  }

  get id() {
    return computed({
      get: () => this._store[GETTERS.GET_ID],
      set: (value) => {
        this._store[ACTIONS.SET_ID](value);
      },
    });
  }

  get parentId() {
    return computed({
      get: () => this._store[GETTERS.GET_PARENT_ID],
      set: (value) => {
        this._store[ACTIONS.SET_PARENT_ID](value);
      },
    });
  }

  get iterationPath() {
    return computed({
      get: () => this._store[GETTERS.GET_ITERATION_PATH],
      set: (value) => {
        this._store[ACTIONS.SET_ITERATION_PATH](value);
      },
    });
  }

  get areaPath() {
    return computed({
      get: () => this._store[GETTERS.GET_AREA_PATH],
      set: (value) => {
        this._store[ACTIONS.SET_AREA_PATH](value);
      },
    });
  }

  get tags() {
    return computed({
      get: () => this._store[GETTERS.GET_TAGS],
      set: (value) => {
        this._store[ACTIONS.SET_TAGS](value);
      },
    });
  }
}
