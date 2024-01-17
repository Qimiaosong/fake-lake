"use strict";(self["webpackChunkdata_lake_analytics"]=self["webpackChunkdata_lake_analytics"]||[]).push([[246],{2246:function(e,a,l){l.r(a),l.d(a,{default:function(){return z}});l(7658);var r=l(6252),o=l(2262),t=l(3577),s=l(9963),u=l(2201),d=l(3907),m=l(3625),c=l(219),n=l(6583);const i=e=>((0,r.dD)("data-v-5446d579"),e=e(),(0,r.Cn)(),e),p=i((()=>(0,r._)("p",{class:"component-heading"},"数据入湖",-1))),_={class:"btn-box"},w={style:{display:"flex","align-items":"center"}},f={style:{margin:"0"}},k={class:"table-cell-btn-box"},b={style:{width:"100%",display:"flex","flex-wrap":"nowrap"}},v={key:0},y={class:"wrap-form"},h={class:"self-row"},U={class:"self-row"},g={key:1},S={class:"wrap-form"},V={class:"self-row"},W={class:"self-row"},x={class:"self-row"},C={key:2},L={class:"wrap-form"},D={class:"self-row"},j={class:"self-row"},O={key:0,class:"log"};var q=(0,r.aZ)({__name:"DataLakeView",setup(e){const a=(0,u.tv)(),l=(0,d.oR)(),i=(0,o.iH)(!1),q=(0,o.iH)(null),N=(0,o.iH)(!1),H=(0,o.iH)(!1),z=(0,o.iH)(null),J=(0,o.iH)(),R=(0,o.iH)("");let T=(0,o.qj)({res:[],dbName:"",tables:[],fields:[]});const F={0:{"source.parallelism":4,"sink.parallelism":4,"job.checkpoint_interval":3e5,server_time_zone:"UTC"},1:{data_consumer_type:0,is_add_partition:0,topic_rex:"",dbname:"",kafka_schema_registry_url:""},2:{table_name:null,range_partition_key:[],hash_partition_key:[],table_hashbucket_count:4,num_executors:4,executor_cores:2,executor_memory:[4,"G"],driver_cores:1,driver_memory:[2,"G"]}},G={name:"",type:0,datasource_type:0,datasource_id:"",datasource_name:"",resource_params:JSON.parse(JSON.stringify(F[0])),description:"",owner_id:1,env_id:-1,is_scheduled:!1,scheduler_info:{type:0,schedule_cron_expression:["*","*","*","*","*"],schedule_interval:1,schedule_type:1}};let I=(0,o.iH)(JSON.parse(JSON.stringify(G)));const M=(0,o.qj)({name:[{validator:n.ym,trigger:"blur",required:!0}],type:[{required:!0,trigger:"blur",message:"不能为空"}],datasource_id:[{required:!0,trigger:"blur",message:"不能为空"}],"resource_params.table_name":[{required:!0,trigger:"blur",message:"不能为空"}]}),K=()=>{l.dispatch("dataLake/getDataLakeTaskList",{searchContent:R.value})},P=(0,r.Fl)((()=>l.state.dataLake.dataLakeList));(0,r.wF)((()=>{K()}));const Y=e=>{i.value=e},Z=()=>{Y(!1)},E=async()=>{await l.dispatch("dataSource/getDataSourceList")},A=(0,r.Fl)((()=>l.state.dataSource.dataSourceList)),B=async e=>{A.value&&A.value?.length>0||await E();const a=A.value?.find((a=>a.name===e));return T.dbName=a?.connection_params?.project_name,a},Q=async e=>{e&&await E()},$=async e=>{const a=await B(e);I.value.datasource_id=a?.id,I.value.datasource_type=a?.type,I.value.resource_params=JSON.parse(JSON.stringify(F[a?.type]))||{}},X=async e=>(T?.dbName||await B(I.value.datasource_name),l.dispatch("dataSource/getDBSchema",{id:e}).then((e=>{1e4===e.data.code?(T.res=e.data.data,T.tables=T.res.find((e=>e.dbname===T?.dbName))?.tables||[]):Object.assign(T,{res:[],dbName:"",tables:[],fields:[]})})).catch((e=>{console.log(e)}))),ee=e=>{e&&X(I.value?.datasource_id)},ae=e=>{T.fields=T.tables?.find((a=>a.name===e))?.fields||[]},le=e=>{for(const a in e)Object.hasOwnProperty.call(I.value.resource_params,a)&&(I.value.resource_params[a]=e[a])},re=e=>{const a={range_partition_key:[],hash_partition_key:[]};le(a),ae(e)},oe=async e=>{e&&(N.value&&e&&await X(I.value?.datasource_id),ae(I.value?.resource_params["table_name"]))},te=((0,r.Fl)((()=>l.state.environment.envList)),async()=>{I.value=JSON.parse(JSON.stringify(G)),N.value=!1,Y(!0)}),se=async()=>{let e=[J.value];(0,n.R2)(e).then((e=>{I.value.scheduler_info=q.value?.formData,l.dispatch("dataLake/createDataLakeTask",{curDataLake:I.value}).then((e=>{10002!=e.data.code&&Y(!1)}))})).catch((e=>{console.log(e)}))},ue=async({row:e})=>{await l.dispatch("dataLake/getDataLakeDetails",e).then((e=>{1e4==e.data.code?I.value=e.data.data:I.value=JSON.parse(JSON.stringify(G))})).catch((e=>{console.log("err",e)})),I.value?.is_scheduled&&q.value?.resetFormDate([{property:"type",defaultValue:0},{property:"schedule_cron_expression",defaultValue:["*","*","*","*","*"]},{property:"schedule_interval",defaultValue:1},{property:"schedule_type",defaultValue:1}]),N.value=!0,Y(!0)},de=async()=>{let e=[J.value];(0,n.R2)(e).then((e=>{I.value.scheduler_info=q.value?.formData,l.dispatch("dataLake/updateDataLakeTask",{curDataLake:I.value}).then((()=>{Y(!1)}))})).catch((e=>{console.log(e)}))},me=({row:e,$index:a})=>{l.dispatch("dataLake/deleteDataLakeTask",{id:e.id})},ce=e=>![null,void 0,""].includes(e),ne=({row:e})=>{l.dispatch("dataLake/startDataLakeTask",{row:e})},ie=({row:e})=>{l.dispatch("dataLake/stopTask",{row:e})},pe=({row:e})=>{l.dispatch("dataLake/resumeTask",{row:e})},_e=({row:e})=>{z.value=null,H.value=!0,l.dispatch("dataLake/viewLog",{id:e.id}).then((e=>{z.value=e.data})).catch((e=>{}))},we=e=>{l.commit("dataLake/SET_PAGE_INFO",{currentPage:e}),K()},fe=(0,n.Ds)((()=>{we(1)}),500),ke=()=>{fe()};return(e,u)=>{const d=(0,r.up)("el-button"),q=(0,r.up)("el-input"),F=(0,r.up)("el-table-column"),G=(0,r.up)("SvgIcon"),K=(0,r.up)("el-tooltip"),E=(0,r.up)("el-table"),B=(0,r.up)("el-form-item"),X=(0,r.up)("el-option"),ae=(0,r.up)("el-select"),le=(0,r.up)("el-input-number"),fe=(0,r.up)("el-switch"),be=(0,r.up)("el-row"),ve=(0,r.up)("el-form"),ye=(0,r.up)("el-empty"),he=(0,r.up)("el-drawer"),Ue=(0,r.Q2)("permission");return(0,r.wg)(),(0,r.iD)("div",null,[p,(0,r._)("div",_,[(0,r.wy)(((0,r.wg)(),(0,r.j4)(d,{class:"create-btn",type:"primary",onClick:te},{default:(0,r.w5)((()=>[(0,r.Uk)("添加入湖任务")])),_:1})),[[Ue,"create"]]),(0,r.Wm)(q,{modelValue:R.value,"onUpdate:modelValue":u[0]||(u[0]=e=>R.value=e),onInput:ke,placeholder:"根据名称查询"},null,8,["modelValue"])]),(0,r.Wm)(E,{data:(0,o.SU)(P),style:{width:"100%"}},{default:(0,r.w5)((()=>[(0,r.Wm)(F,{prop:"name",label:"名称"}),(0,r.Wm)(F,{prop:"datasource_type",label:"类型",formatter:(0,o.SU)(n.rv)},null,8,["formatter"]),(0,r.Wm)(F,{prop:"status",label:"任务启动状态"},{default:(0,r.w5)((e=>[(0,r._)("div",w,[(0,r._)("div",{style:(0,t.j5)({width:"6px",height:"6px",backgroundColor:(0,o.SU)(n.HR)(e.row.status)?.color,borderRadius:"50%",marginRight:"5px"})},null,4),(0,r._)("p",f,(0,t.zw)((0,o.SU)(n.HR)(e.row.status)?.text),1)])])),_:1}),(0,r.Wm)(F,{prop:"updated_at",label:"更新日期",formatter:(0,o.SU)(n.lI)},null,8,["formatter"]),(0,r.Wm)(F,{prop:"operation",label:"操作"},{default:(0,r.w5)((e=>[(0,r._)("div",k,[(0,r.Wm)(K,{effect:"dark",content:"编辑",placement:"top",offset:2,"popper-class":"el-popper-low"},{default:(0,r.w5)((()=>[(0,r.wy)(((0,r.wg)(),(0,r.j4)(d,{size:"small",circle:"",onClick:(0,s.iM)((a=>ue(e)),["stop"]),class:"icon-button"},{default:(0,r.w5)((()=>[(0,r.Wm)(G,{name:"edit",stroke:"var(--el-color-primary)"})])),_:2},1032,["onClick"])),[[Ue,"update"]])])),_:2},1024),(0,r.Wm)(K,{effect:"dark",content:"删除",placement:"top",offset:2,"popper-class":"el-popper-low"},{default:(0,r.w5)((()=>[(0,r.wy)(((0,r.wg)(),(0,r.j4)(d,{size:"small",circle:"",onClick:(0,s.iM)((a=>(0,o.SU)(n.qK)(e,me)),["stop"]),disabled:0==e.row.status||1==e.row.status,class:"icon-button"},{default:(0,r.w5)((()=>[(0,r.Wm)(G,{name:"delete",stroke:"#f56c6c"})])),_:2},1032,["onClick","disabled"])),[[Ue,"delete"]])])),_:2},1024),(0,r.Wm)(K,{effect:"dark",content:"启动任务",placement:"top",offset:2,"popper-class":"el-popper-low"},{default:(0,r.w5)((()=>[-1===[0,1,5].indexOf(e.row.status)?((0,r.wg)(),(0,r.j4)(d,{key:0,size:"small",circle:"",onClick:(0,s.iM)((a=>ne(e)),["stop"]),class:"icon-button"},{default:(0,r.w5)((()=>[(0,r.Wm)(G,{name:"start",stroke:"var(--el-color-primary)"})])),_:2},1032,["onClick"])):(0,r.kq)("",!0)])),_:2},1024),(0,r.Wm)(K,{effect:"dark",content:"停止任务",placement:"top",offset:2,"popper-class":"el-popper-low"},{default:(0,r.w5)((()=>[-1!=[0,1].indexOf(e.row.status)?((0,r.wg)(),(0,r.j4)(d,{key:0,size:"small",circle:"",onClick:(0,s.iM)((a=>ie(e)),["stop"]),class:"icon-button"},{default:(0,r.w5)((()=>[(0,r.Wm)(G,{name:"pause",stroke:"var(--el-color-primary)"})])),_:2},1032,["onClick"])):(0,r.kq)("",!0)])),_:2},1024),(0,r.Wm)(K,{effect:"dark",content:"继续任务",placement:"top",offset:2,"popper-class":"el-popper-low"},{default:(0,r.w5)((()=>[-1!=[5].indexOf(e.row.status)?((0,r.wg)(),(0,r.j4)(d,{key:0,size:"small",circle:"",onClick:(0,s.iM)((a=>pe(e)),["stop"]),class:"icon-button"},{default:(0,r.w5)((()=>[(0,r.Wm)(G,{name:"play",stroke:"var(--el-color-primary)"})])),_:2},1032,["onClick"])):(0,r.kq)("",!0)])),_:2},1024),(0,r.Wm)(K,{effect:"dark",content:"日志",placement:"top",offset:2,"popper-class":"el-popper-low"},{default:(0,r.w5)((()=>[(0,r.Wm)(d,{size:"small",circle:"",onClick:(0,s.iM)((a=>_e(e)),["stop"]),disabled:-1==e.row.status,class:"icon-button"},{default:(0,r.w5)((()=>[(0,r.Wm)(G,{name:"log",stroke:"var(--el-color-primary)"})])),_:2},1032,["onClick","disabled"])])),_:2},1024)])])),_:1})])),_:1},8,["data"]),(0,r.Wm)(m.Z,{show:i.value,onHandleShow:u[25]||(u[25]=e=>Y(!1))},{popup:(0,r.w5)((()=>[(0,r.Wm)(ve,{model:(0,o.SU)(I),rules:M,ref_key:"ruleFormRef",ref:J,"label-width":"250px"},{default:(0,r.w5)((()=>[(0,r.Wm)(B,{label:"名称",prop:"name"},{default:(0,r.w5)((()=>[(0,r.Wm)(q,{modelValue:(0,o.SU)(I).name,"onUpdate:modelValue":u[1]||(u[1]=e=>(0,o.SU)(I).name=e),disabled:N.value},null,8,["modelValue","disabled"])])),_:1}),(0,r.Wm)(B,{label:"数据源",prop:"datasource_name"},{default:(0,r.w5)((()=>[(0,r._)("div",b,[(0,r.Wm)(ae,{modelValue:(0,o.SU)(I).datasource_name,"onUpdate:modelValue":u[2]||(u[2]=e=>(0,o.SU)(I).datasource_name=e),onChange:$,onVisibleChange:Q,placeholder:"请选择","no-data-text":"没有数据"},{default:(0,r.w5)((()=>[((0,r.wg)(!0),(0,r.iD)(r.HY,null,(0,r.Ko)((0,o.SU)(A),((e,a)=>((0,r.wg)(),(0,r.j4)(X,{key:a,value:e.name},null,8,["value"])))),128))])),_:1},8,["modelValue"]),(0,r.Wm)(d,{onClick:u[3]||(u[3]=e=>(0,o.SU)(a).push("/home/dataSource")),style:{"margin-left":"10px"}},{default:(0,r.w5)((()=>[(0,r.Uk)("还没有？去添加")])),_:1})])])),_:1}),0==(0,o.SU)(I).datasource_type?((0,r.wg)(),(0,r.iD)("div",v,[(0,r.Wm)(B,{label:"运行资源配置"},{default:(0,r.w5)((()=>[(0,r._)("div",y,[(0,r._)("div",h,[(0,r.Wm)(B,{label:"source并行度"},{default:(0,r.w5)((()=>[(0,r.Wm)(le,{modelValue:(0,o.SU)(I).resource_params["source.parallelism"],"onUpdate:modelValue":u[4]||(u[4]=e=>(0,o.SU)(I).resource_params["source.parallelism"]=e),min:1,"controls-position":"right"},null,8,["modelValue"])])),_:1}),(0,r.Wm)(B,{label:"sink并行度"},{default:(0,r.w5)((()=>[(0,r.Wm)(le,{modelValue:(0,o.SU)(I).resource_params["sink.parallelism"],"onUpdate:modelValue":u[5]||(u[5]=e=>(0,o.SU)(I).resource_params["sink.parallelism"]=e),min:1,"controls-position":"right"},null,8,["modelValue"])])),_:1})]),(0,r._)("div",U,[(0,r.Wm)(B,{label:"checkpoint存储时间间隔(/ms)"},{default:(0,r.w5)((()=>[(0,r.Wm)(q,{modelValue:(0,o.SU)(I).resource_params["job.checkpoint_interval"],"onUpdate:modelValue":u[6]||(u[6]=e=>(0,o.SU)(I).resource_params["job.checkpoint_interval"]=e)},null,8,["modelValue"])])),_:1}),(0,r.Wm)(B,{label:"数据库时区"},{default:(0,r.w5)((()=>[(0,r.Wm)(q,{modelValue:(0,o.SU)(I).resource_params["server_time_zone"],"onUpdate:modelValue":u[7]||(u[7]=e=>(0,o.SU)(I).resource_params["server_time_zone"]=e)},null,8,["modelValue"])])),_:1})])])])),_:1})])):1==(0,o.SU)(I).datasource_type?((0,r.wg)(),(0,r.iD)("div",g,[(0,r.Wm)(B,{label:"运行资源配置"},{default:(0,r.w5)((()=>[(0,r._)("div",S,[(0,r._)("div",V,[(0,r.Wm)(B,{label:"同步历史数据"},{default:(0,r.w5)((()=>[(0,r.Wm)(fe,{modelValue:(0,o.SU)(I).resource_params["data_consumer_type"],"onUpdate:modelValue":u[8]||(u[8]=e=>(0,o.SU)(I).resource_params["data_consumer_type"]=e),"active-value":1,"inactive-value":0},null,8,["modelValue"])])),_:1}),(0,r.Wm)(B,{label:"增加时间分区列"},{default:(0,r.w5)((()=>[(0,r.Wm)(fe,{modelValue:(0,o.SU)(I).resource_params["is_add_partition"],"onUpdate:modelValue":u[9]||(u[9]=e=>(0,o.SU)(I).resource_params["is_add_partition"]=e),"active-value":1,"inactive-value":0},null,8,["modelValue"])])),_:1})]),(0,r._)("div",W,[(0,r.Wm)(B,{label:"topic正则表达式",prop:"resource_params.topic_rex",rules:{required:!0,trigger:"blur",message:"不能为空"}},{default:(0,r.w5)((()=>[(0,r.Wm)(q,{modelValue:(0,o.SU)(I).resource_params["topic_rex"],"onUpdate:modelValue":u[10]||(u[10]=e=>(0,o.SU)(I).resource_params["topic_rex"]=e)},null,8,["modelValue"])])),_:1}),(0,r.Wm)(B,{label:"数据库名",prop:"resource_params.dbname",rules:{required:!0,trigger:"blur",message:"不能为空"}},{default:(0,r.w5)((()=>[(0,r.Wm)(q,{modelValue:(0,o.SU)(I).resource_params["dbname"],"onUpdate:modelValue":u[11]||(u[11]=e=>(0,o.SU)(I).resource_params["dbname"]=e)},null,8,["modelValue"])])),_:1})]),(0,r._)("div",x,[(0,r.Wm)(B,{label:"registry服务"},{default:(0,r.w5)((()=>[(0,r.Wm)(q,{modelValue:(0,o.SU)(I).resource_params["kafka_schema_registry_url"],"onUpdate:modelValue":u[12]||(u[12]=e=>(0,o.SU)(I).resource_params["kafka_schema_registry_url"]=e),placeholder:"请输入url"},null,8,["modelValue"])])),_:1})])])])),_:1})])):2===(0,o.SU)(I).datasource_type?((0,r.wg)(),(0,r.iD)("div",C,[(0,r.Wm)(B,{label:"表名",prop:"resource_params.table_name"},{default:(0,r.w5)((()=>[(0,r.Wm)(ae,{modelValue:(0,o.SU)(I).resource_params["table_name"],"onUpdate:modelValue":u[13]||(u[13]=e=>(0,o.SU)(I).resource_params["table_name"]=e),onChange:re,onVisibleChange:ee,placeholder:"请选择"},{default:(0,r.w5)((()=>[((0,r.wg)(!0),(0,r.iD)(r.HY,null,(0,r.Ko)((0,o.SU)(T).tables,((e,a)=>((0,r.wg)(),(0,r.j4)(X,{key:a,label:e.name,value:e.name},null,8,["label","value"])))),128))])),_:1},8,["modelValue"])])),_:1}),(0,r.Wm)(B,{label:"Range分区",prop:"resource_params.range_partition_key"},{default:(0,r.w5)((()=>[(0,r.Wm)(ae,{modelValue:(0,o.SU)(I).resource_params["range_partition_key"],"onUpdate:modelValue":u[14]||(u[14]=e=>(0,o.SU)(I).resource_params["range_partition_key"]=e),onVisibleChange:oe,disabled:!ce((0,o.SU)(I)?.resource_params["table_name"]),multiple:"",clearable:"",placeholder:"请选择"},{default:(0,r.w5)((()=>[((0,r.wg)(!0),(0,r.iD)(r.HY,null,(0,r.Ko)((0,o.SU)(T).fields,((e,a)=>((0,r.wg)(),(0,r.j4)(X,{key:a,label:e.name,value:e.name},null,8,["label","value"])))),128))])),_:1},8,["modelValue","disabled"])])),_:1}),(0,r.Wm)(B,{label:"主键",prop:"resource_params.hash_partition_key"},{default:(0,r.w5)((()=>[(0,r.Wm)(ae,{modelValue:(0,o.SU)(I).resource_params["hash_partition_key"],"onUpdate:modelValue":u[15]||(u[15]=e=>(0,o.SU)(I).resource_params["hash_partition_key"]=e),onVisibleChange:oe,disabled:!ce((0,o.SU)(I).resource_params["table_name"]),multiple:"",clearable:"",placeholder:"请选择"},{default:(0,r.w5)((()=>[((0,r.wg)(!0),(0,r.iD)(r.HY,null,(0,r.Ko)((0,o.SU)(T).fields,((e,a)=>((0,r.wg)(),(0,r.j4)(X,{key:a,label:e.name,value:e.name},null,8,["label","value"])))),128))])),_:1},8,["modelValue","disabled"])])),_:1}),(0,o.SU)(I).resource_params["hash_partition_key"]&&(0,o.SU)(I).resource_params["hash_partition_key"]?.length?((0,r.wg)(),(0,r.j4)(B,{key:0,label:"主键分桶数",prop:"resource_params.table_hashbucket_count"},{default:(0,r.w5)((()=>[(0,r.Wm)(le,{modelValue:(0,o.SU)(I).resource_params["table_hashbucket_count"],"onUpdate:modelValue":u[16]||(u[16]=e=>(0,o.SU)(I).resource_params["table_hashbucket_count"]=e),min:1,"controls-position":"right"},null,8,["modelValue"])])),_:1})):(0,r.kq)("",!0),(0,r.Wm)(B,{label:"运行资源配置"},{default:(0,r.w5)((()=>[(0,r._)("div",L,[(0,r._)("div",D,[(0,r.Wm)(B,{label:"执行器cpu数",prop:"resource_params.executor_cores"},{default:(0,r.w5)((()=>[(0,r.Wm)(le,{modelValue:(0,o.SU)(I).resource_params["executor_cores"],"onUpdate:modelValue":u[17]||(u[17]=e=>(0,o.SU)(I).resource_params["executor_cores"]=e),min:1,"controls-position":"right"},null,8,["modelValue"])])),_:1}),(0,o.SU)(I).resource_params["executor_memory"]?((0,r.wg)(),(0,r.j4)(B,{key:0,label:"执行器内存大小",prop:"resource_params.executor_memory",class:"nowrap-form-item"},{default:(0,r.w5)((()=>[(0,r.Wm)(le,{modelValue:(0,o.SU)(I).resource_params["executor_memory"][0],"onUpdate:modelValue":u[18]||(u[18]=e=>(0,o.SU)(I).resource_params["executor_memory"][0]=e),min:1,"controls-position":"right"},null,8,["modelValue"]),(0,r.Wm)(ae,{modelValue:(0,o.SU)(I).resource_params["executor_memory"][1],"onUpdate:modelValue":u[19]||(u[19]=e=>(0,o.SU)(I).resource_params["executor_memory"][1]=e),placeholder:"单位",class:"unit-el-select"},{default:(0,r.w5)((()=>[(0,r.Wm)(X,{value:"G",label:"G"})])),_:1},8,["modelValue"])])),_:1})):(0,r.kq)("",!0)]),(0,r._)("div",j,[(0,r.Wm)(B,{label:"驱动器cpu数",prop:"resource_params.driver_cores"},{default:(0,r.w5)((()=>[(0,r.Wm)(le,{modelValue:(0,o.SU)(I).resource_params["driver_cores"],"onUpdate:modelValue":u[20]||(u[20]=e=>(0,o.SU)(I).resource_params["driver_cores"]=e),min:1,"controls-position":"right"},null,8,["modelValue"])])),_:1}),(0,o.SU)(I).resource_params["driver_memory"]?((0,r.wg)(),(0,r.j4)(B,{key:0,label:"驱动器内存大小",prop:"resource_params.driver_memory",placeholder:"单位",class:"nowrap-form-item"},{default:(0,r.w5)((()=>[(0,r.Wm)(le,{modelValue:(0,o.SU)(I).resource_params["driver_memory"][0],"onUpdate:modelValue":u[21]||(u[21]=e=>(0,o.SU)(I).resource_params["driver_memory"][0]=e),min:1,"controls-position":"right"},null,8,["modelValue"]),(0,r.Wm)(ae,{modelValue:(0,o.SU)(I).resource_params["driver_memory"][1],"onUpdate:modelValue":u[22]||(u[22]=e=>(0,o.SU)(I).resource_params["driver_memory"][1]=e),placeholder:"单位",class:"unit-el-select"},{default:(0,r.w5)((()=>[(0,r.Wm)(X,{value:"G",label:"G"})])),_:1},8,["modelValue"])])),_:1})):(0,r.kq)("",!0)]),(0,r.Wm)(be,{class:"self-row"},{default:(0,r.w5)((()=>[(0,r.Wm)(B,{label:"执行器数",prop:"resource_params.num_executors"},{default:(0,r.w5)((()=>[(0,r.Wm)(le,{modelValue:(0,o.SU)(I).resource_params["num_executors"],"onUpdate:modelValue":u[23]||(u[23]=e=>(0,o.SU)(I).resource_params["num_executors"]=e),min:1,"controls-position":"right"},null,8,["modelValue"])])),_:1})])),_:1})])])),_:1})])):(0,r.kq)("",!0),(0,r.Wm)(B,{label:"描述"},{default:(0,r.w5)((()=>[(0,r.Wm)(q,{modelValue:(0,o.SU)(I).description,"onUpdate:modelValue":u[24]||(u[24]=e=>(0,o.SU)(I).description=e),type:"textarea"},null,8,["modelValue"])])),_:1}),(0,r.Wm)(B,null,{default:(0,r.w5)((()=>[N.value?((0,r.wg)(),(0,r.j4)(d,{key:1,type:"primary",onClick:de},{default:(0,r.w5)((()=>[(0,r.Uk)("更新")])),_:1})):((0,r.wg)(),(0,r.j4)(d,{key:0,type:"primary",onClick:se},{default:(0,r.w5)((()=>[(0,r.Uk)("创建")])),_:1})),(0,r.Wm)(d,{onClick:Z},{default:(0,r.w5)((()=>[(0,r.Uk)("取消")])),_:1})])),_:1})])),_:1},8,["model","rules"])])),_:1},8,["show"]),(0,r.Wm)(c.Z,{module:(0,o.SU)(l).state.dataLake.pageInfo,onChangePage:we},null,8,["module"]),(0,r.Wm)(he,{modelValue:H.value,"onUpdate:modelValue":u[26]||(u[26]=e=>H.value=e),title:"日志",direction:"rtl",size:"60%"},{default:(0,r.w5)((()=>[z.value?((0,r.wg)(),(0,r.iD)("pre",O,(0,t.zw)(z.value),1)):((0,r.wg)(),(0,r.j4)(ye,{key:1,description:"空"}))])),_:1},8,["modelValue"])])}}}),N=l(3744);const H=(0,N.Z)(q,[["__scopeId","data-v-5446d579"]]);var z=H}}]);
//# sourceMappingURL=246.14a2917e.js.map