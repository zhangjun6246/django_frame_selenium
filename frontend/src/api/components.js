import request from '@/utils/request'

// 获取项目列表
export function projectsList(page) {
  return request({
    url: '/projects/',
    method: 'get',
    params: page
  })
}

// 创建新项目
export function createProject(form) {
  return request({
    url: '/projects/',
    method: 'post',
    data: form
  })
}
