# fpga/build.tcl
# Run in Vivado: vivado -mode batch -source build.tcl
create_project pdm_fpga_accel ./vivado_out -part xc7z020clg400-1 -force
add_files ./axi_matmul.v
update_compile_order -fileset sources_1
# Synthesis & Implementation steps (commented for speed)
# launch_runs synth_1 -jobs 4
# wait_on_run synth_1
puts "FPGA Project Created Successfully!"