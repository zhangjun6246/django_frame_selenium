import axios from 'axios'

// 创建axios实例
const service = axios.create({
  baseURL: process.env.BASE_API, // api的base_url
  timeout: 5000// 请求超时时间
})

// download url
const downloadUrl = url => {
  const iframe = document.createElement('iframe')
  iframe.style.display = 'none'
  iframe.src = url
  iframe.onload = function() {
    document.body.removeChild(iframe)
  }
  document.body.appendChild(iframe)
}

// request拦截器
service.interceptors.request.use(
  config => {
    // if (localStorage.token) {
    //   config.headers.Authorization = `token ${localStorage.token}`// 让每个请求携带自定义token 请根据实际情况自行修改
    // }
    return config
  }, error => {
    return Promise.reject(error)
  })

// respone拦截器
service.interceptors.response.use(
  response => {
    if (response.headers && response.headers['content-type'] === 'application/vnd.android.package-archive') {
      // 判断返回的'content-type'如果符合android安装包的调用downloadUrl的iframe下载文件;
      const res = downloadUrl(response.request.responseURL)
      return res
    } else {
      return response
    }
  },
  error => {
    // if (error.response) {
    //     switch (error.response.status) {
    //         case 401:
    //             // 返回 401 清除token信息并跳转到登录页面
    //             localStorage.removeItem('token')
    //             localStorage.removeItem('username')
    //             router.replace({
    //                 path: '/login',
    //                 query: {redirect: router.currentRoute.fullPath}
    //             })
    //     }
    // }
    return Promise.reject(error.response.data)// 返回接口返回的错误信息
  }
)

export default service
