<template>
  <div class="app-container">
    <div class="button-container" style="padding-bottom:20px;">
      <el-button class="button-item" style="margin-left: 10px;" @click="projectCreate" type="primary" v-if='userName === "admin"'>
        <i class="el-icon-document"></i> 创建新项目
      </el-button>
    </div>

    <el-table :data="list" border fit highlight-current-row style="width: 100%">
      <el-table-column align="center" type="index" label='id'></el-table-column>
      <el-table-column align="center" label="项目名称" prop="name"></el-table-column>
      <el-table-column align="center" label="平台类型" prop="platform_set">
        <template slot-scope="scope">
          <el-tag 
            v-for="item in scope.row.platform_set" :key="item" :type="item | typeFilter" hit="true">{{item | typeTranFilter}}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作">
        <template slot-scope="scope">
          <el-button size="small" round type="info" @click="handleVersion(scope.row)" v-if='userProject.indexOf(scope.row.name) > -1 || userProject === ""'>版本管理</el-button>
          <el-button size="small" round type="info" @click="handleModule(scope.row)" v-if='userProject.indexOf(scope.row.name) > -1 || userProject === ""'>模块管理</el-button>
          <el-button size="small" round type="warning" @click="handleUpdate(scope.row)" v-if='userName === "admin"'><i class="el-icon-edit"></i> 编辑</el-button>
          <el-button size="small" round type="danger" @click="handleDelete(scope.row)" v-if='userName === "admin"'><i class="el-icon-delete"></i> 删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog :title="textProjectMap[dialogStatus]" :visible.sync="projectFormVisible" style="margin-top:-3%;width:75%;margin-left:10%;">
      <el-form class="small-space" :model="projectForm" label-position="left" label-width="100px" style='width: 65%; margin-left:10%;'>
        <el-form-item label="项目名称">
          <el-input  placeholder="请输入项目名称" v-model="projectForm.name"></el-input>
        </el-form-item>
        <el-form-item label="平台类型">
          <el-select v-model="projectForm.platform_set" multiple placeholder="请选择平台类型" style="width:100%;">
            <el-option v-for="item in PLATFORM_TYPE" :key="item.key"
              :label="item.display_name" :value="item.key">
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="projectFormVisible = false">取 消</el-button>
        <el-button v-if="dialogStatus=='create'" type="primary" @click="create">确 定</el-button>
        <el-button v-else type="primary" @click="update">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
const PLATFORM_TYPE = [
  { key: 'android', display_name: 'Android' },
  { key: 'ios', display_name: 'Ios' },
  { key: 'pc', display_name: 'PC' },
  { key: 'm', display_name: 'M' },
  { key: 'interface', display_name: '接口' },
  { key: 'perforance', display_name: '性能' }
]

import { projectsList } from '@/api/components'

export default {
  name: 'project',
  data() {
    return {
      userName: 'admin',
      userProject: '',
      list: null,
      total: null,
      projectPage: 1,
      versionTotal: 0,
      versionPage: 1,
      moduleTotal: 0,
      modulePage: 1,
      verList: null,
      modList: null,
      projectForm: {
        id: '',
        name: ''
      },
      projectFormVisible: false,
      versionFormVisible: false,
      versionTableVisible: false,
      moduleFormVisible: false,
      moduleTableVisible: false,
      dialogStatus: '',
      PLATFORM_TYPE,
      textProjectMap: {
        update: '编辑项目',
        create: '创建项目'
      },
      textVerMap: {
        update: '编辑版本',
        create: '创建版本'
      },
      textModuleMap: {
        update: '编辑模块',
        create: '创建模块'
      }
    }
  },
  filters: {
    typeFilter(type) {
      const typeMap = {
        android: 'warning',
        ios: 'warning',
        pc: 'success',
        m: 'success'
      }
      return typeMap[type]
    },

    typeTranFilter(type) {
      const typeTranMap = {
        android: 'Android',
        ios: 'Ios',
        interface: '接口',
        perforance: '性能',
        pc: 'PC',
        m: 'M'
      }
      return typeTranMap[type]
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      projectsList({ page: this.projectPage }).then(res => {
        if (res.status === 200) {
          this.list = res.data.results
          this.total = res.data.count
        } else {
          this.$message({
            type: 'error',
            message: '获取列表失败,接口请求异常'
          })
          this.getList()
        }
      })
    },
    projectCreate() {
      this.dialogStatus = 'create'
      this.projectFormVisible = true
    },
    update() {
      console.log('111')
    },
    create() {
      console.log('111')
    }
  }
}
</script>

