# verilogModuleAddPrefix

verilog/SystemVerilog module add prefix script 

可用于ysyx项目添加学号

```bash
# usage
python3 verilogAutoPrefix.py "$(VERILOG_SRC_DIR)" "$(PREFIX)" "$(IGNORE_NAME)"
# for ysyx project:
python3 verilogAutoPrefix.py "$(VERILOG_SRC_DIR)" "$(STUID)_" "$(STUID)"
```
